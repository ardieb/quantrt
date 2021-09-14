from abc import ABCMeta, abstractmethod
from datetime import datetime


class Miner(meta=ABCMeta):
    """A `Miner` is a class that mines historical market data.
    All `Miner` implementations implement an asynchronous `run` method
    which performs the mining operation and saves all the data to the
    database. The `Miner` will not return any data.
    """
    def __init__(self, name: str):
        self.name = name

    @abstractmethod
    async def run(self, tstamp: datetime):
        """Run the market mining operation. Store any data to the database.
        :param tstamp: datetime - the current time.
        """
        raise NotImplementedError()
    