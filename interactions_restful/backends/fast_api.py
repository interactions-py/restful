from typing import Callable, Coroutine

from fastapi import FastAPI as _FastAPI
from uvicorn import Config, Server

from ..abc import BaseApi

__all__ = ("FastAPI", )


class FastAPI(BaseApi):
    def __init__(self, host: str, port: int, **kwargs):
        self.host = host
        self.port = port

        self.app = _FastAPI(**kwargs)
        self._config = Config(self.app, host=self.host, port=self.port)

    def add_route(self, coro: Callable[..., Coroutine], endpoint: str, method: str, **kwargs):
        self.app.router.add_api_route(
            endpoint,
            coro,
            methods=[method],
            **kwargs
        )

    async def run(self):
        server = Server(config=self._config)
        await server.serve()
