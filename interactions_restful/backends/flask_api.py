from typing import Callable, Coroutine

from flask import Flask, Blueprint

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
        self.debug = kwargs.pop("debug", False)

        self.app: Flask = Flask(kwargs.pop("import_name", None) or "interactions_restful", **kwargs)

    def add_endpoint_method(self, coro: Callable[..., Coroutine], endpoint: str, method: str, **kwargs):
        self.app.route(endpoint, methods=[method], **kwargs)(coro)

    @staticmethod
    def create_router(**kwargs):
        return FlaskRouter(kwargs.pop("name"), **kwargs)

    def add_router(self, router: FlaskRouter):
        self.app.register_blueprint(router.blueprint)

    async def run(self):
        self.app.run(self.host, self.port, self.debug)
