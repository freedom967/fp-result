import abc
from dataclasses import dataclass
from typing import Any, Callable, Generic, NoReturn, TypeVar

T = TypeVar("T")
E = TypeVar("E", str, Exception)
MappedT = TypeVar("MappedT")


class Result(abc.ABC, Generic[T]):
    @classmethod
    def Ok(cls, value: T) -> "Ok[T]":
        return Ok(value)

    @classmethod
    def err(cls, error: E) -> "Err":
        return Err(error)

    @abc.abstractmethod
    def map(self, f: Callable[[T], MappedT]) -> "Result[MappedT]":
        pass

    @abc.abstractmethod
    def and_then(self, f: Callable[[T], "Result[MappedT]"]) -> "Result[MappedT]":
        pass

    @abc.abstractmethod
    def unwrap(self) -> T:
        pass

    @abc.abstractmethod
    def is_error(self) -> bool:
        pass

    @abc.abstractmethod
    def is_ok(self) -> bool:
        pass


@dataclass
class Ok(Result[T]):
    _data: T

    def __init__(self, value: T) -> None:
        self._data = value

    def map(self, f: Callable[[T], MappedT]) -> "Ok[MappedT]":
        return Ok(f(self._data))

    def and_then(self, f: Callable[[T], Result[MappedT]]) -> Result[MappedT]:
        return f(self._data)

    def unwrap(self) -> T:
        return self._data

    def __repr__(self) -> str:
        return f"class Ok({self._data})"

    def is_error(self) -> bool:
        return False

    def is_ok(self) -> bool:
        return True


@dataclass
class Err(Result[Any]):
    _error: Exception

    def __init__(self, error: E) -> None:
        if isinstance(error, str):
            self._error = Exception(error)
        else:
            self._error = error

    def map(self, f: Callable) -> "Err":
        return self

    def and_then(self, f: Callable[[Any], Result[MappedT]]) -> Result[MappedT]:
        return self

    def unwrap(self) -> NoReturn:
        raise self._error

    def is_error(self) -> bool:
        return True

    def is_ok(self) -> bool:
        return False
