import inspect
from typing import TYPE_CHECKING

from interactions import Client, listen
from interactions.api.events import ExtensionLoad, ExtensionUnload

if TYPE_CHECKING:
    from .abc import BaseAPIHandler

__all__ = ("APIManager",)


class APIManager:
    def __init__(self, bot: Client, backend: "BaseAPIHandler") -> None:
        self.bot = bot
        self.bot.api = self
        self.backend = backend

        self.bot.add_listener(self.extension_load.copy_with_binding(self))
        self.bot.add_listener(self.extension_unload.copy_with_binding(self))

    @listen(ExtensionLoad)
    async def extension_load(self, event: ExtensionLoad):
        if getattr(event.extension, "router", None) is None:
            event.extension.router = self.backend.create_router(name=event.extension.name)

        callables = inspect.getmembers(
            event.extension, predicate=lambda x: getattr(x, "__api__", False)
        )

        for _, callback in callables:
            data: dict = callback.__api__
            event.extension.router.add_endpoint_method(
                callback, data["endpoint"], data["method"], **data["kwargs"]
            )

        # print(self.backend)
        self.backend.add_router(event.extension.router)

    @listen(ExtensionUnload)
    async def extension_unload(self, event: ExtensionUnload):
        if getattr(event.extension, "router", None):
            self.backend.remove_router(event.extension.router)
