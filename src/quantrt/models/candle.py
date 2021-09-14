import asyncio
import asyncpg

import quantrt.common.config
import quantrt.common.log
import quantrt.util.database
import quantrt.util.time

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from typing import Optional, Iterable

from quantrt.common.timescale import Timescale


__all__ = ["Candle", "save", "save_batch", "fetch", "fetch_batch"]


@dataclass
class Candle:
    # The product ticker.
    product: str
    # The tstamp where this candle started tracking.
    tstamp: datetime
    # The granularity at which this candle captures information.
    timescale: Timescale
    # The opening price of the candle.
    open: Decimal
    # The highest price of the candle.
    high: Decimal
    # The lowest price of the candle.
    low: Decimal
    # The close price of the candle.
    close: Decimal
    # The volume traded during the candle timespan, in the native currency.
    volume: Decimal


async def save(candle: Candle, pool: Optional[asyncpg.Pool] = None):
    if not pool:
        pool = quantrt.common.config.db_conn_pool
    if not pool:
        quantrt.common.log.QuantrtLog.exception("No connection pool has been configured.")
        raise EnvironmentError("No connection pool has been configured.")

    async with pool.acquire() as conn:
        sql = """
            INSERT INTO candle 
                (product, tstamp, timescale, open, high, low, close, volume)
            VALUES 
                ($1, $2, $3, $4, $5, $6, $7, $8)
            ON CONFLICT 
                (product, tstamp, timescale) 
            DO UPDATE
            SET 
                open = EXCLUDED.open,
                high = EXCLUDED.high,
                low = EXCLUDED.low,
                close = EXCLUDED.close,
                volume = EXCLUDED.volume
        """
        statement = await quantrt.util.database.prepare_sql(sql, conn)
        await statement.executemany((
            candle.product, 
            candle.tstamp, 
            candle.timescale.name, 
            candle.open, 
            candle.high, 
            candle.low, 
            candle.close, 
            candle.volume))


async def save_batch(candles: Iterable[Candle], pool: Optional[asyncpg.Pool] = None):
    if not pool:
        pool = quantrt.common.config.db_conn_pool
    if not pool:
        quantrt.common.log.QuantrtLog.exception("No connection pool has been configured.")
        raise EnvironmentError("No connection pool has been configured.")
    
    async with pool.acquire() as conn:
        sql = """
            INSERT INTO candle 
                (product, tstamp, timescale, open, high, low, close, volume)
            VALUES 
                ($1, $2, $3, $4, $5, $6, $7, $8)
            ON CONFLICT 
                (product, tstamp, timescale) 
            DO UPDATE
            SET 
                open = EXCLUDED.open,
                high = EXCLUDED.high,
                low = EXCLUDED.low,
                close = EXCLUDED.close,
                volume = EXCLUDED.volume
        """
        statement = await quantrt.util.database.prepare_sql(sql, conn)
        await statement.executemany([(
            candle.product, 
            candle.tstamp, 
            candle.timescale.name, 
            candle.open, 
            candle.high, 
            candle.low, 
            candle.close, 
            candle.volume) for candle in candles])


async def fetch(product: str, tstamp: datetime, timescale: Timescale, pool: Optional[asyncpg.Pool] = None) -> Candle:
    if not pool:
        pool = quantrt.common.config.db_conn_pool
    if not pool:
        quantrt.common.log.QuantrtLog.exception("No connection pool has been configured.")
        raise EnvironmentError("No connection pool has been configured.")

    tstamp = quantrt.util.time.datetime_floor(tstamp, timescale)
    async with pool.acquire() as conn:
        sql = """
            SELECT * FROM candle WHERE product = $1 AND tstamp = $2 AND timescale = $3
        """
        statement = await quantrt.util.database.prepare_sql(sql, conn)
        row = await statement.fetch(product, tstamp, timescale.name)
    
    return Candle(
        product=row[0]["product"],
        tstamp=row[0]["tstamp"],
        timescale=Timescale(row[0]["timescale"]),
        open=row[0]["open"],
        high=row[0]["high"],
        low=row[0]["low"],
        close=row[0]["close"],
        volume=row[0]["volume"]
    )


async def fetch_batch(product: str, start: datetime, stop: datetime, timescale: Timescale, pool: Optional[asyncpg.Pool] = None) -> Iterable[Candle]:
    if not pool:
        pool = quantrt.common.config.db_conn_pool
    if not pool:
        quantrt.common.log.QuantrtLog.exception("No connection pool has been configured.")
        raise EnvironmentError("No connection pool has been configured.")

    start = quantrt.util.time.datetime_floor(start, timescale)
    stop = quantrt.util.time.datetime_floor(stop, timescale)

    async with pool.acquire() as conn:
        sql = """
            SELECT * FROM candle WHERE product = $1 AND (tstamp => $2 AND tstamp <= $3) AND timescale = $4
        """
        statement = await quantrt.util.database.prepare_sql(sql, conn)
        rows = await statement.fetch(product, start, stop, timescale.name)
    
    return [Candle(
        product=row["product"],
        tstamp=row["tstamp"],
        timescale=Timescale(row["timescale"]),
        open=row["open"],
        high=row["high"],
        low=row["low"],
        close=row["close"],
        volume=row["volume"]
    ) for row in rows]
