import abc
from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeVar

T = TypeVar("T")
MappedT = TypeVar("MappedT")


class Option(abc.ABC, Generic[T]):
    @classmethod
    def some(cls, value: T) -> "Some[T]":
        return Some(value)

    @classmethod
    def NoneValue(cls) -> "NoneValue":
        return NoneValue()

    @abc.abstractmethod
    def map(self, f: Callable[[T], MappedT]) -> "Option[MappedT]":
        pass

    @abc.abstractmethod
    def and_then(self, f: Callable[[T], "Option[MappedT]"]) -> "Option[MappedT]":
        pass

    @abc.abstractmethod
    def unwrap(self) -> T:
        pass

    def unwrap_or(self, new_value: T) -> T:
        if isinstance(self, Some):
            return self._value
        else:
            return new_value

    @abc.abstractmethod
    def expect(self, msg: str) -> T:
        pass

    @abc.abstractmethod
    def is_some(self) -> bool:
        pass

    @abc.abstractmethod
    def is_none(self) -> bool:
        pass


@dataclass
class Some(Option[T]):
    def __init__(self, value: T) -> None:
        self._value: T = value

    def map(self, f: Callable[[T], MappedT]) -> Option[MappedT]:
        return Some(f(self._value))

    def and_then(self, f: Callable[[T], Option[MappedT]]) -> Option[MappedT]:
        return f(self._value)

    def unwrap(self) -> T:
        return self._value

    def expect(self, msg: str) -> T:
        return self._value

    def __repr__(self) -> str:
        return f"class Some({self._value})"

    def is_some(self) -> bool:
        return True

    def is_none(self) -> bool:
        return False


@dataclass
class NoneValue(Option[Any]):
    def map(self, f: Callable[..., MappedT]) -> Option[MappedT]:
        return self

    def unwrap(self):
        raise ValueError("unwrap on None")

    def and_then(self, f: Callable[[Any], Option[MappedT]]) -> Option[MappedT]:
        return self

    def expect(self, msg):
        raise ValueError(msg)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, NoneValue)

    def is_some(self) -> bool:
        return False

    def is_none(self) -> bool:
        return True
