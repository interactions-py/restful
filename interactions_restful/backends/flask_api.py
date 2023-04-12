from typing import Callable, Coroutine

try:
    from asgiref.wsgi import WsgiToAsgi
    from hypercorn.config import Config
    from hypercorn.asyncio import serve
    from flask import Flask, Blueprint
except ImportError as e:
    raise ImportError("Flask dependencies weren't installed. Please, install they with [flask] option") from e

from ..abc import BaseApi, BaseRouter

__all__ = ("FlaskAPI", "FlaskRouter")


class FlaskRouter(BaseRouter):
    def __init__(self, name: str, **kwargs):
        self.blueprint = Blueprint(name.lower(), name, **kwargs)

    def add_endpoint_method(self, coro: Callable[..., Coroutine], endpoint: str, method: str, **kwargs):
        self.blueprint.route(endpoint, methods=[method], **kwargs)(coro)


class FlaskAPI(BaseApi):
    def __init__(self, host: str, port: int, **kwargs):
        self.host = host
        self.port = port

        self.app: Flask = Flask(kwargs.pop("import_name", None) or "interactions_restful", **kwargs)
        self._config = Config()
        self._config.bind = [f"{host}:{port}"]

    def add_endpoint_method(self, coro: Callable[..., Coroutine], endpoint: str, method: str, **kwargs):
        self.app.route(endpoint, methods=[method], **kwargs)(coro)

    @staticmethod
    def create_router(**kwargs):
        return FlaskRouter(kwargs.pop("name"), **kwargs)

    def add_router(self, router: FlaskRouter):
        self.app.register_blueprint(router.blueprint)

    async def run(self):
        await serve(WsgiToAsgi(self.app), self._config)
