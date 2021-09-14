import coinbasepro

from dataclasses import dataclass
from typing import TypeVar, Collection, Union, NewType


__all__ = ["REST", "OneOrMany", "is_one", "is_many"]


T = TypeVar("T")

OneOrMany = Union[T, Collection[T]]
REST = coinbasepro.AuthenticatedClient
Symbol = NewType("Symbol", str)


@dataclass
class Product:
    base: Symbol
    quote: Symbol

    def __str__(self) -> str:
        return "{}-{}".format(self.base, self.quote)
    
    def __repr__(self) -> str:
        return "Product: {}".format(self.__str__())


def is_one(t: OneOrMany[T]) -> bool:
    return not isinstance(t, Collection)


def is_many(t: OneOrMany[T]) -> bool:
    return isinstance(t, Collection)
    