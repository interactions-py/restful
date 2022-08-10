import asyncio
from typing import Optional

from interactions.ext.base import Base
from interactions.ext.version import Version, VersionAuthor

from .main import APIClient, route

from interactions import Client, Extension


__all__ = ["version", "base", "SimpleAPI", "APIClient", "route", "setup"]

version = Version(
    version="0.0.1", author=VersionAuthor(name="Damego", email="damego.dev@gmail.com")
)

base = Base(
    name="interactions-fastapi",
    version=version,
    description="Build an API for your bot with FastAPI",
    link="https://github.com/interactions-py/interactions-fastapi",
    packages=["interactions.ext.fastapi"],
    requirements=[
        "discord-py-interactions",
        "fastapi",
        "uvicorn"
    ],
)


class SimpleAPI(Extension):
    def __init__(self, client: Client, host: Optional[str] = "127.0.0.1", port: Optional[int] = 32512, **kwargs):
        self.client = client
        self._loop = client._loop
        self._api = APIClient(host, port, **kwargs)
        self.client.api = self

        self.route = self._api.route

        self.get = self._api.app.get
        self.post = self._api.app.post
        self.put = self._api.app.put
        self.delete = self._api.app.delete
        self.options = self._api.app.options
        self.head = self._api.app.head
        self.patch = self._api.app.patch
        self.trace = self._api.app.trace
        self.websocket = self._api.app.websocket

        self.__override_client()

    def __override_client(self):
        self.client.start = self._client_start

    def __register_extensions_routes(self):
        for ext in self.client._extensions.values():
            if not isinstance(ext, Extension):
                continue
            _dir = dir(ext)
            for attr in _dir:
                if attr.startswith("__") and attr.endswith("__"):
                    continue
                func = getattr(ext, attr)
                if hasattr(func, "__api_route__"):
                    method, path, kwargs = func.__api_route__
                    self.route(method, path, **kwargs)(func)
                elif hasattr(func, "__api_ws__"):
                    path, name = func.__api_ws__
                    self.websocket(path, name)(func)

    async def _run_api(self):
        await self._api.run()

        self.bot_task.cancel()  # TODO: do something with this

    def _client_start(self):
        """
        Function for overriding ``interactions.Client.start`` method.
        """
        self.__register_extensions_routes()

        self.ipc_task = self._loop.create_task(self._run_api())
        self.bot_task = self._loop.create_task(self.client._ready())
        gather = asyncio.gather(self.ipc_task, self.bot_task)

        try:
            self._loop.run_until_complete(gather)
        except asyncio.exceptions.CancelledError:
            pass


def setup(
    client: Client,
    host: Optional[str] = "127.0.0.1",
    port: Optional[int] = 32512,
    **kwargs,
):
    """
    Setup an FastAPI to your bot.
    """
    return SimpleAPI(client, host, port, **kwargs)
