import asyncio
import asyncpg
import json

import quantrt.common.config
import quantrt.common.log
import quantrt.util.database
import quantrt.util.time

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, Iterable, Dict

from quantrt.common.timescale import Timescale


__all__ = ["save", "save_batch", "fetch", "fetch_batch"]


@dataclass
class Indicator:
    # Product identifier
    product: str
    # Timestamp for the indicator.
    timestamp: datetime
    # Timescale at which the indicator was calculated.
    timescale: Timescale
    # Name of the indicator.
    name: str
    # Values calculated stored as json, user's responsibility to keep track
    # of which are which.
    values: Dict


async def save(indicator: Indicator, pool: Optional[asyncpg.Pool] = None):
    if not pool:
        pool = quantrt.common.config.db_conn_pool
    if not pool:
        quantrt.common.log.QuantrtLog.exception("No connection pool has been configured.")
        raise EnvironmentError("No connection pool has been configured.")

    async with pool.acquire() as conn:
        values = json.dumps(indicator.values)
        sql = """
            INSERT INTO indicator 
                (product, timestamp, timescale, name, values)
            VALUES 
                ($1, $2, $3, $4, $5)
            ON CONFLICT 
                (product, timestamp, timescale, name) 
            DO UPDATE
            SET 
                values = EXCLUDED.values
        """
        statement = await quantrt.util.database.prepare_sql(sql, conn)
        await statement.executemany((
            indicator.product, 
            indicator.timestamp, 
            indicator.timescale.name, 
            indicator.name, 
            values))


async def save_batch(indicators: Iterable[Indicator], pool: Optional[asyncpg.Pool] = None):
    if not pool:
        pool = quantrt.common.config.db_conn_pool
    if not pool:
        quantrt.common.log.QuantrtLog.exception("No connection pool has been configured.")
        raise EnvironmentError("No connection pool has been configured.")

    async with pool.acquire() as conn:
        sql = """
            INSERT INTO indicator 
                (product, timestamp, timescale, name, values)
            VALUES 
                ($1, $2, $3, $4, $5)
            ON CONFLICT 
                (product, timestamp, timescale, name) 
            DO UPDATE
            SET 
                values = EXCLUDED.values
        """
        statement = await quantrt.util.database.prepare_sql(sql, conn)
        await statement.executemany([(
            indicator.product, 
            indicator.timestamp, 
            indicator.timescale.name, 
            indicator.name, 
            json.dumps(indicator.values)) for indicator in indicators])


async def fetch(product: str, name: str, timestamp: datetime, timescale: Timescale, pool: Optional[asyncpg.Pool] = None) -> Indicator:
    if not pool:
        pool = quantrt.common.config.db_conn_pool
    if not pool:
        quantrt.common.log.QuantrtLog.exception("No connection pool has been configured.")
        raise EnvironmentError("No connection pool has been configured.")

    timestamp = quantrt.util.time.datetime_floor(timestamp, timescale)

    async with pool.acquire() as conn:
        sql = """
            SELECT * FROM indicator WHERE product = $1 AND timestamp = $2 AND timescale = $3 AND name = $4
        """
        statement = await quantrt.util.database.prepare_sql(sql, conn)
        row = await statement.fetchrow(product, timestamp, timescale.name, name)
    
    return Indicator(
        product=row["product"],
        timestamp=row["timestamp"],
        timescale=Timescale(row["timescale"]),
        name=row["name"],
        values=json.loads(row["values"]))


async def fetch_batch(product: str, name: str, start: datetime, stop: datetime, timescale: Timescale, pool: Optional[asyncpg.Pool] = None) -> Iterable[Indicator]:
    if not pool:
        pool = quantrt.common.config.db_conn_pool
    if not pool:
        quantrt.common.log.QuantrtLog.exception("No connection pool has been configured.")
        raise EnvironmentError("No connection pool has been configured.")

    start = quantrt.util.time.datetime_floor(start, timescale)
    stop = quantrt.util.time.datetime_floor(stop, timescale)

    async with pool.acquire() as conn:
        sql = """
            SELECT * FROM indicator WHERE product = $1 AND (timestamp => $2 AND timestamp <= $3) AND timescale = $4 AND name = $5
        """
        statement = await quantrt.util.database.prepare_sql(sql, conn)
        rows = await statement.fetch(product, start, stop, timescale.name, name)
    
    return [Indicator(
        product=row["product"],
        timestamp=row["timestamp"],
        timescale=Timescale(row["timescale"]),
        name=row["name"],
        values=json.loads(row["values"])) for row in rows]
