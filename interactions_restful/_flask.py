from typing import Callable, Coroutine

from asgiref.wsgi import WsgiToAsgi
from hypercorn.config import Config
from hypercorn.asyncio import serve
from flask import Flask

from .abc import BaseApi

__all__ = ("FlaskAPI")


class FlaskAPI(BaseApi):
    def __init__(self, host: str, port: int, **kwargs):
        self.host = host
        self.port = port

        self.app: Flask = Flask(kwargs.pop("import_name", None) or "interactions_restful", **kwargs)
        self._config = Config()
        self._config.bind = [f"{host}:{port}"]

    def add_route(self, coro: Callable[..., Coroutine], endpoint: str, method: str, **kwargs):
        self.app.route(endpoint, methods=[method], **kwargs)(coro)

    async def run(self):
        await serve(WsgiToAsgi(self.app), self._config)
