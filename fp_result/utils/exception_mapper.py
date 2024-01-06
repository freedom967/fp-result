from typing import Any, Callable, Coroutine, ParamSpec, TypeVar

from fp_result.result import Err, Ok, Result

T = TypeVar("T")
P = ParamSpec("P")


def map_exception(func: Callable[P, T]) -> Callable[P, Result[T]]:
    def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[T]:
        try:
            return Ok(func(*args, **kwargs))
        except Exception as e:
            return Err(e)

    return wrapper


def map_async_exception(
    func: Callable[P, Coroutine[Any, Any, T]],
) -> Callable[P, Coroutine[Any, Any, Result[T]]]:
    async def wrapper(*args: P.args, **kwargs: P.kwargs) -> Result[T]:
        try:
            res = await func(*args, **kwargs)
            return Ok(res)
        except Exception as e:
            return Err(e)

    return wrapper
