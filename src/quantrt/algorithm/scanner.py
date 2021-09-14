from abc import ABCMeta, abstractmethod
from datetime import datetime
from typing import List, Coroutine


class Scanner(meta=ABCMeta):
    """A Scanner is run on realtime or backtest time input to determine a
    list of actionable product tickers.
    """
    def __init__(self, name: str):
        self.name = name


    @abstractmethod
    async def run(self, tstamp: datetime) -> Coroutine[List[int]]:
        """Run the scanner at the time provided.
        :param tstamp: datetime - the time at which to run the scanner, may be live or backtest.
        :return: List[str] - a list of actionable products.
        """
        raise NotImplementedError()
