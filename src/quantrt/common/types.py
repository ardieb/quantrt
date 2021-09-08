import coinbasepro

from typing import TypeVar, Collection, Union


__all__ = ["REST", "OneOrMany", "is_one", "is_many"]


T = TypeVar("T")

OneOrMany = Union[T, Collection[T]]
REST = coinbasepro.AuthenticatedClient


def is_one(t: OneOrMany[T]) -> bool:
    return not isinstance(t, Collection)


def is_many(t: OneOrMany[T]) -> bool:
    return isinstance(t, Collection)
    