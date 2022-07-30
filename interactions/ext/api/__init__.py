import asyncio
from functools import wraps

from interactions import Client, Extension
from interactions.ext.base import Base
from interactions.ext.version import Version, VersionAuthor

from .main import APIClient, route

__all__ = ["version", "base", "SimpleAPI", "APIClient", "route", "setup"]

version = Version(
    version="0.0.1", author=VersionAuthor(name="Damego", email="danyabatueff@gmail.com")
)

base = Base(
    name="simple_api",
    version=version,
    description="REST api for your bot",
    link="https://github.com/Damego/interactions-simple-api",
    packages=["interactions.ext.api"],
    requirements=[
        "discord-py-interactions",
    ],
)


class SimpleAPI(Extension):
    def __init__(self, client: Client, host: str = "127.0.0.1", port: 32512 = None, **kwargs):
        self.client = client
        self._loop = client._loop
        self._api = APIClient(host, port, **kwargs)
        self.route = self._api.route
        self.websocket = self._api.websocket

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
    host: str = "127.0.0.1",
    port: int = 32512,
    **kwargs,
):
    """
    Setup API to your bot.
    You can also do `bot.load("interactions.ext.api")`
    """
    return SimpleAPI(client, host, port, **kwargs)
