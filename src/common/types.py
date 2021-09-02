from typing import TypeVar, Iterable, Union


__all__ = ["OneOrMany", "is_one", "is_many"]


T = TypeVar('T')

OneOrMany = Union[T, Iterable[T]]


def is_one(t: OneOrMany[T]) -> bool:
    return isinstance(t, T)


def is_many(t: OneOrMany[T]) -> bool:
    return isinstance(t, Iterable[T])