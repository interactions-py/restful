from typing import Callable, Coroutine

from fastapi import APIRouter, FastAPI
from interactions import Client

from ..abc import BaseAPIHandler, BaseRouterWrapper

__all__ = ("FastAPIHandler",)


class FastAPIRouterWrapper(BaseRouterWrapper):
    def __init__(self, **kwargs):
        kwargs.pop("name")  # neccessary only for quart
        self.api_router = APIRouter(**kwargs)

    def add_endpoint_method(
        self, coro: Callable[..., Coroutine], endpoint: str, method: str, **kwargs
    ):
        self.api_router.add_api_route(endpoint, coro, methods=[method], **kwargs)


class FastAPIHandler(BaseAPIHandler):
    app: FastAPI

    def __init__(self, bot: Client, app: FastAPI):
        super().__init__(bot, app)
        self.app.add_event_handler("startup", self.startup)
        self.app.add_event_handler("shutdown", self.shutdown)

    @staticmethod
    def create_router(**kwargs):
        return FastAPIRouterWrapper(**kwargs)

    def add_router(self, router: FastAPIRouterWrapper):
        self.app.include_router(router.api_router)

    def remove_router(self, router: FastAPIRouterWrapper):
        paths_to_check = frozenset(
            f"{router.api_router.prefix}{r.path}" for r in router.api_router.routes
        )
        for i, r in enumerate(self.app.router.routes):
            if r.path in paths_to_check:  # type: ignore
                del self.app.router.routes[i]

    def add_endpoint_method(
        self, coro: Callable[..., Coroutine], endpoint: str, method: str, **kwargs
    ):
        self.app.add_api_route(endpoint, coro, methods=[method], **kwargs)
