from functools import wraps
from typing import Optional

from fastapi import FastAPI
from uvicorn import Config, Server

__all__ = ["APIClient", "route", "websocket"]


class APIClient:
    def __init__(self, host: Optional[str] = "127.0.0.1", port: Optional[int] = 32512, **kwargs):
        self.host = host
        self.port = port
        self.app = FastAPI(**kwargs)

    def route(self, method: str, path: str, **kwargs):
        method = method.lower()
        func = getattr(self.app, method, None)
        if func is None:
            raise AttributeError(f"Method {method} not found!")
        return func(path, **kwargs)

    async def run(self):
        config = Config(self.app, host=self.host, port=self.port)
        server = Server(config=config)
        await server.serve()


@wraps(APIClient.route)
def route(method: str, path: str, **kwargs):
    def wrapper(func):
        func.__api_route__ = (method, path, kwargs)
        return func

    return wrapper


@wraps(FastAPI.websocket)
def websocket(path: str, name: Optional[str] = None):
    def wrapper(func):
        func.__api_ws__ = (path, name)
        return func

    return wrapper
