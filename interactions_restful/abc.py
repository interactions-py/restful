from abc import ABC, abstractmethod
from typing import Callable, Coroutine

__all__ = ("BaseApi", "BaseRouter")


class BaseRouter(ABC):
    @abstractmethod
    def add_endpoint_method(self, coro: Callable[..., Coroutine], endpoint: str, method: str, **kwargs):
        pass


class BaseApi(ABC):
    @abstractmethod
    def __init__(self, host: str, port: int, **kwargs):
        pass

    @abstractmethod
    def add_endpoint_method(self, coro: Callable[..., Coroutine], endpoint: str, method: str, **kwargs):
        pass

    @staticmethod
    @abstractmethod
    def create_router(**kwargs) -> BaseRouter:
        pass

    def add_router(self, router: BaseRouter):
        pass

    @abstractmethod
    async def run(self):
        pass
