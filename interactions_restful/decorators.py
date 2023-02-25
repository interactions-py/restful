import typing

from interactions import Absent, MISSING

__all__ = ("route",)


def route(method: str, endpoint: Absent[str] = MISSING, **kwargs):
    def wrapper(coro: typing.Callable[..., typing.Coroutine]):
        coro.__api__ = {
            "method": method,
            "endpoint": endpoint or coro.__name__,
            "kwargs": kwargs
        }

        return coro
    return wrapper
