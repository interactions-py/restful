import asyncio
from threading import Thread
from inspect import getmembers
from typing import Type, TypeVar

from interactions import Client

from .abc import BaseApi

__all__ = ("APIExtension", )
API_TYPE = TypeVar("API_TYPE", bound=BaseApi)


class APIClient:
    bot: Client

    def __init__(self, bot: Client, api: Type[API_TYPE], host: str, port: int, **kwargs) -> None:
        self.bot = bot
        self.bot.api = self

        self.client: API_TYPE = api(host, port, **kwargs)

        self.bot.async_startup_tasks.append((self.run, (), {}))

    async def run(self):
        self._register_extension_routes()

        thread = Thread(target=self._run_api_thread_worker)
        thread.start()

    def _run_api_thread_worker(self):
        asyncio.run(self.client.run())

    def _register_extension_routes(self):
        for extension in self.bot.ext.values():
            for _, coro in getmembers(extension, predicate=asyncio.iscoroutinefunction):
                if not hasattr(coro, "__api__"):
                    continue
                data = coro.__api__
                self.client.add_route(coro, data["endpoint"], data["method"], **data["kwargs"])


