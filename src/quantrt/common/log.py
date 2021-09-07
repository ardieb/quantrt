import datetime
import logging
import sys

from typing import Any


__all__ = ["QuantrtLog"]

logger = logging.getLogger('quantrtlog')
formatter = logging.Formatter("[%(name)s] @ %(asctime)s from %(funcName)s with level %(levelname)s: %(message)s")
console_stream = logging.StreamHandler(stream = sys.stderr)
console_stream.setFormatter(formatter)
file_stream = logging.FileHandler(f"logs/quantrt-log-{datetime.datetime.now().date()}")
file_stream.setFormatter(formatter)

logger.addHandler(console_stream)
logger.addHandler(file_stream)


class QuantrtLog:

    @classmethod
    def info(cls, message: Any, *args: Any):
        logger.info(message, *args)


    @classmethod
    def debug(cls, message: Any, *args: Any):
        logger.debug(message, *args)


    @classmethod
    def warn(cls, message: Any, *args: Any):
        logger.warn(message, *args)


    @classmethod
    def warning(cls, message: Any, *args: Any):
        logger.warning(message, *args)


    @classmethod
    def error(cls, message: Any, *args: Any):
        logger.error(message, *args)

    
    @classmethod
    def exception(cls, message: Any, *args: Any):
        logger.exception(message, *args)


    @classmethod
    def set_level(cls, level: int):
        logger.setLevel(level)

    
    @classmethod
    def get_level(cls) -> int:
        return logger.level
