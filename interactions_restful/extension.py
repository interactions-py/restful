from asyncio import iscoroutinefunction
from inspect import getmembers
from typing import overload, Literal

from interactions.models.internal import Extension
from interactions import Client

from .abc import BaseApi

__all__ = ("APIExtension", )


class APIExtension(Extension):
    bot: Client

    @overload
    def __init__(
        self,
        bot: Client,
        host: str,
        port: int, 
        mode: Literal["flask"],
        *,
        import_name: str | None = None,
        **kwargs
    ):
        pass

    @overload
    def __init__(
        self,
        bot: Client,
        host: str,
        port: int, 
        mode: Literal["fastapi"], 
        **kwargs
    ):
        pass

    def __init__(self, bot, host: str, port: int, mode: str, **kwargs) -> None:
        self.bot.api = self

        self.client: BaseApi = None
        match mode:
            case "flask":
                from ._flask import FlaskAPI
                self.client = FlaskAPI(host, port, **kwargs)
            case "fastapi":
                from ._fastapi import FastAPI
                self.client = FastAPI(host, port, **kwargs)

        self.bot.async_startup_tasks.append((self.run, (), {}))

    async def run(self):
        for extension in self.bot.ext.values():
            for _, coro in getmembers(extension, predicate=iscoroutinefunction):
                if not hasattr(coro, "__api__"):
                    continue
                data = coro.__api__
                self.client.add_route(coro, data["endpoint"], data["method"], **data["kwargs"])

        await self.client.run()

