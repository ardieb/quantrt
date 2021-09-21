from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import Coroutine


__all__ = ["Strategy"]


class Strategy(meta=ABCMeta):
    """A Strategy is run on realtime or backtest time input and a
    list of actionable products to determine actions to take.
    """
    def __init__(self, name: str):
        self.name = name


    @abstractmethod
    async def scan(self, tstamp: datetime) -> Coroutine:
        """Run the scanner at the time provided.
        :param tstamp: datetime - the time at which to run the scanner, may be live or backtest.
        """
        raise NotImplementedError()

    
    @abstractmethod
    async def act(self, tstamp: datetime) -> Coroutine:
        """Produce a set of actions at the time provided.
        :param tstamp: datetime - the time at which to run the strategy, may be live or backtest.
        """
        raise NotImplementedError()
