from abc import ABC, abstractclassmethod
from typing import Callable, Coroutine

__all__ = ("BaseApi")


class BaseApi(ABC):
    @abstractclassmethod
    def add_route(self, coro: Callable[..., Coroutine], endpoint: str, method: str, **kwargs):
        pass

    @abstractclassmethod
    async def run(self):
        pass