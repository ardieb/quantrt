from abc import ABCMeta, abstractmethod
from datetime import datetime
from dataclasses import dataclass
from decimal import Decimal
from enum import Enum
from typing import List, Coroutine, Union


__all__ = [
    "Nothing",
    "MarketBuy",
    "MarketSell",
    "LimitBuy",
    "LimitSell",
    "StopLimitBuy",
    "StopLimitSell",
    "Action",
    "Strategy"
]


class Nothing:
    pass


@dataclass
class MarketBuy:
    product: str
    amount: Decimal


@dataclass
class MarketSell:
    product: str
    amount: Decimal


@dataclass
class LimitBuy:
    product: str
    amount: Decimal
    price: Decimal


@dataclass
class LimitSell:
    product: str
    amount: Decimal
    price: Decimal


@dataclass
class StopLimitBuy:
    product: str
    stop: Decimal
    price: Decimal
    amount: Decimal


@dataclass
class StopLimitSell:
    product: str
    stop: Decimal
    price: Decimal
    amount: Decimal


Action = Union[Nothing, MarketBuy, MarketSell, LimitBuy, LimitSell, StopLimitBuy, StopLimitSell]


class Strategy(meta=ABCMeta):
    """A Strategy is run on realtime or backtest time input and a
    list of actionable products to determine actions to take.
    """
    def __init__(self, name: str):
        self.name = name


    @abstractmethod
    async def run(self, tstamp: datetime, products: List[str]) -> Coroutine[List[Action]]:
        """Run the scanner at the time provided.
        :param tstamp: datetime - the time at which to run the scanner, may be live or backtest.
        :return: List[str] - a list of actionable products.
        """
        raise NotImplementedError()
        