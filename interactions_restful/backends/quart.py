from typing import Callable, Coroutine

from interactions import Client
from quart import Blueprint, Quart
from werkzeug.routing.matcher import State

from ..abc import BaseAPIHandler, BaseRouterWrapper

__all__ = ("QuartAPIHandler", "QuartBlueprintWrapper")


class QuartBlueprintWrapper(BaseRouterWrapper):
    def __init__(self, name: str, **kwargs):
        self.blueprint = Blueprint(name.lower(), name, **kwargs)
        self.endpoints: list[str] = []

    def add_endpoint_method(
        self, coro: Callable[..., Coroutine], endpoint: str, method: str, **kwargs
    ):
        self.blueprint.route(endpoint, methods=[method], **kwargs)(coro)
        self.endpoints.append(coro.__name__)


class QuartAPIHandler(BaseAPIHandler):
    app: Quart

    def __init__(self, bot: Client, app: Quart):
        super().__init__(bot, app)
        self.app.while_serving(self.while_serving_task)

    async def while_serving_task(self):
        await self.startup()
        yield
        await self.shutdown()

    @staticmethod
    def create_router(**kwargs):
        return QuartBlueprintWrapper(kwargs.pop("name"), **kwargs)

    def add_router(self, router: QuartBlueprintWrapper):
        self.app.register_blueprint(router.blueprint)

    def _recursive_remove(self, endpoint: str, state: State):
        for rule in state.rules.copy():
            if rule.endpoint == endpoint:
                state.rules.remove(rule)

        for substate in state.static.values():
            self._recursive_remove(endpoint, substate)

    def remove_router(self, router: QuartBlueprintWrapper):
        blueprint = self.app.blueprints.pop(router.blueprint.name)

        for endpoint in router.endpoints:
            endpoint = f".{blueprint.name}.{endpoint.removeprefix('/')}".lstrip(".")
            self.app.url_map._rules_by_endpoint.pop(endpoint, None)  # type: ignore
            self.app.view_functions.pop(endpoint, None)

            self._recursive_remove(endpoint, self.app.url_map._matcher._root)

    def add_endpoint_method(
        self, coro: Callable[..., Coroutine], endpoint: str, method: str, **kwargs
    ):
        self.app.route(endpoint, methods=[method], **kwargs)(coro)
