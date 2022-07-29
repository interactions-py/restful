import asyncio
from functools import wraps

from fastapi import FastAPI
from uvicorn import Config, Server
import interactions

__all__ = ["APIClient", "route"]


class APIClient:
    def __init__(self, client: interactions.Client, host: str = "127.0.0.1", port: int = 32512, **kwargs):
        self.client = client
        self.loop = self.client._loop
        self.host = host
        self.port = port
        self.app = FastAPI(**kwargs)
        self.ipc_task = self.bot_task = None

    def route(self, method: str, path: str, **kwargs):
        method = method.lower()
        func = getattr(self.app, method, None)
        if func is None:
            raise AttributeError(f"Method {method} not found!")
        return func(path, **kwargs)

    async def _start(self):
        config = Config(self.app, host=self.host, port=self.port)
        server = Server(config=config)
        await server.serve()

        self.bot_task.cancel()

    def __register_extensions_routes(self):
        for ext in self.client._extensions.values():
            if not isinstance(ext, interactions.Extension):
                continue
            _dir = dir(ext)
            for attr in _dir:
                if attr.startswith("__") and attr.endswith("__"):
                    continue
                func = getattr(ext, attr)
                if hasattr(func, "__ipc__"):
                    method, path, kwargs = func.__ipc__
                    self.route(method, path, **kwargs)(func)

    def start(self):
        self.__register_extensions_routes()

        self.ipc_task = self.loop.create_task(self._start())
        self.bot_task = self.loop.create_task(self.client._ready())
        gather = asyncio.gather(self.ipc_task, self.bot_task)

        try:
            self.loop.run_until_complete(gather)
        except asyncio.exceptions.CancelledError:
            pass


@wraps(IPCServer.route)
def route(method: str, path: str, **kwargs):
    def wrapper(func):
        func.__ipc__ = (method, path, kwargs)
        return func
    return wrapper
