import asyncio
import inspect
from asyncio import Task
from typing import Any, Callable, Coroutine, Protocol

from interactions import CallbackObject, Client

from .manager import APIManager

__all__ = ("BaseAPIHandler", "BaseRouterWrapper")


class BaseRouterWrapper(Protocol):
    def add_endpoint_method(
        self, coro: Callable[..., Coroutine], endpoint: str, method: str, **kwargs
    ):
        ...


class BaseAPIHandler:
    bot: Client
    app: Any
    task: Task | None
    api_client: APIManager

    def __init__(self, bot: Client, app: Any):
        self.bot = bot
        self.app = app
        self.task = None
        self.api_client = APIManager(self.bot, self)

        # there's a problem deferring starting up the bot to an asgi server -
        # sys.modules[__main__] will be replaced with the asgi server's module
        # this means any files that were in the file where the bot is will be lost

        # we can't actually fully work around this - not perfectly, anyway
        # what we can somewhat rely on is that people are using the api wrappers
        # in their main file - you could place it somewhere else, but why would
        # you want to?
        # regardless, we exploit this by getting the module of the caller of the
        # api wrapper - in this, we have to go two calls back because the subclasses
        # count as a call
        # we can then use that module as the module to get the commands from during startup
        stack = inspect.stack()
        self.__original_module = inspect.getmodule(stack[2][0])

    @staticmethod
    def create_router(**kwargs) -> BaseRouterWrapper:
        ...

    def add_router(self, router: BaseRouterWrapper):
        ...

    def remove_router(self, router: BaseRouterWrapper):
        ...

    def add_endpoint_method(
        self, coro: Callable[..., Coroutine], endpoint: str, method: str, **kwargs
    ):
        ...

    async def startup(self):
        commands = inspect.getmembers(
            self.__original_module, lambda x: isinstance(x, CallbackObject)
        )
        for command in commands:
            self.bot.add_command(command[1])

        route_callables = inspect.getmembers(
            self.__original_module, predicate=lambda x: getattr(x, "__api__", False)
        )
        for callable in route_callables:
            callback = callable[1]
            data: dict = callback.__api__
            self.add_endpoint_method(callback, data["endpoint"], data["method"], **data["kwargs"])

        self.task = asyncio.create_task(self.bot.astart())

    async def shutdown(self):
        await self.bot.stop()
        if self.task:
            self.task.cancel()
