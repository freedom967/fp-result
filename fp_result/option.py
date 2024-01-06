import abc
from dataclasses import dataclass
from typing import Any, Callable, Generic, TypeAlias, TypeVar

T = TypeVar("T")
MappedT = TypeVar("MappedT")


class OptionBase(abc.ABC, Generic[T]):
    @classmethod
    def some(cls, value: T) -> "Some[T]":
        return Some(value)

    @classmethod
    def NoneType(cls) -> "NoneValue":
        return NoneValue()

    @abc.abstractmethod
    def map(self, f: Callable[[T], MappedT]) -> "OptionBase[MappedT]":
        pass

    @abc.abstractmethod
    def and_then(
        self, f: Callable[[T], "OptionBase[MappedT]"]
    ) -> "OptionBase[MappedT]":
        pass

    @abc.abstractmethod
    def unwrap(self) -> T:
        pass

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
class Some(OptionBase[T]):
    def __init__(self, value: T) -> None:
        self._value: T = value

    def map(self, f: Callable[[T], MappedT]) -> OptionBase[MappedT]:
        return Some(f(self._value))

    def and_then(self, f: Callable[[T], OptionBase[MappedT]]) -> OptionBase[MappedT]:
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
class NoneValue(OptionBase[Any]):
    def map(self, f: Callable[..., MappedT]) -> OptionBase[MappedT]:
        return self

    def unwrap(self):
        raise ValueError("unwrap on None")

    def and_then(self, f: Callable[[Any], OptionBase[MappedT]]) -> OptionBase[MappedT]:
        return self

    def expect(self, msg):
        raise ValueError(msg)

    def __eq__(self, __value: object) -> bool:
        return isinstance(__value, NoneValue)

    def is_some(self) -> bool:
        return False

    def is_none(self) -> bool:
        return True


Option: TypeAlias = Some[T] | NoneValue
