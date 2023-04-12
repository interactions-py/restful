from typing import Callable, Coroutine

from fastapi import FastAPI as _FastAPI, APIRouter
from uvicorn import Config, Server

from ..abc import BaseApi, BaseRouter

__all__ = ("FastAPI", )


class FastApiRouter(BaseRouter):
    def __init__(self, **kwargs):
        self.api_router = APIRouter(**kwargs)

    def add_endpoint_method(self, coro: Callable[..., Coroutine], endpoint: str, method: str, **kwargs):
        self.api_router.add_api_route(
            endpoint,
            coro,
            methods=[method],
            **kwargs
        )


class FastAPI(BaseApi):
    def __init__(self, host: str, port: int, **kwargs):
        self.host = host
        self.port = port

        self.app = _FastAPI(**kwargs)
        self._config = Config(self.app, host=self.host, port=self.port)

    def add_endpoint_method(self, coro: Callable[..., Coroutine], endpoint: str, method: str, **kwargs):
        self.app.router.add_api_route(
            endpoint,
            coro,
            methods=[method],
            **kwargs
        )

    @staticmethod
    def create_router(**kwargs) -> BaseRouter:
        return FastApiRouter(**kwargs)

    def add_router(self, router: FastApiRouter):
        self.app.include_router(router.api_router)

    async def run(self):
        server = Server(config=self._config)
        await server.serve()
