from abc import ABC, abstractmethod
from typing import Callable, Coroutine

__all__ = ("BaseApi", )


class BaseApi(ABC):
    @abstractmethod
    def __init__(self, host: str, port: int, **kwargs):
        pass

    @abstractmethod
    def add_route(self, coro: Callable[..., Coroutine], endpoint: str, method: str, **kwargs):
        pass

    @abstractmethod
    async def run(self):
        pass