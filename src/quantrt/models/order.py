import asyncio
import asyncpg

import quantrt.common.config
import quantrt.common.log
import quantrt.util.database
import quantrt.util.time

from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal
from enum import Enum
from typing import Optional, Iterator


__all__ = ["OrderStatus", "Order", "save", "save_batch", "fetch", "fetch_batch", "fetch_open"]


class OrderStatus(Enum):
    Open = "open"
    Maker = "maker"
    Taker = "taker"
    Canceled = "canceled"


@dataclass
class Order:
    # order id from coinbase
    order_id: str
    # Product ticker.
    product: str
    # Timestamp of the trade.
    timestamp: datetime
    # Order status
    status: OrderStatus
    # Which side?
    side: str
    # What was the trade size?
    amount: Decimal
    # Price.
    price: Decimal


async def save(order: Order, pool: Optional[asyncpg.Pool] = None):
    if not pool:
        pool = quantrt.common.config.db_conn_pool
    if not pool:
        quantrt.common.log.QuantrtLog.exception("No connection pool has been configured.")
        raise EnvironmentError("No connection pool has been configured.")

    async with pool.acquire() as conn:
        sql = """
            INSERT INTO order 
                (id, product, timestamp, status, side, amount, price)
            VALUES 
                ($1, $2, $3, $4, $5, $6, $7)
            ON CONFLICT 
                (product, order_id) 
            DO UPDATE
            SET
                timestamp = EXCLUDED.timestamp,
                status = EXCLUDED.status,
                side = EXCLUDED.side,
                amount = EXCLUDED.amount,
                price = EXCLUDED.price
        """
        statement = await quantrt.util.database.prepare_sql(sql, conn)
        await statement.executemany((
            order.order_id,
            order.product,
            order.timestamp,
            order.status.name,
            order.side,
            order.amount,
            order.price))


async def save_batch(orders: Iterator[Order], pool: Optional[asyncpg.Pool] = None):
    if not pool:
        pool = quantrt.common.config.db_conn_pool
    if not pool:
        quantrt.common.log.QuantrtLog.exception("No connection pool has been configured.")
        raise EnvironmentError("No connection pool has been configured.")

    async with pool.acquire() as conn:
        sql = """
            INSERT INTO order 
                (id, product, timestamp, status, side, amount, price)
            VALUES 
                ($1, $2, $3, $4, $5, $6, $7)
            ON CONFLICT 
                (product, order_id) 
            DO UPDATE
            SET
                timestamp = EXCLUDED.timestamp,
                status = EXCLUDED.status,
                side = EXCLUDED.side,
                amount = EXCLUDED.amount,
                price = EXCLUDED.price
        """
        statement = await quantrt.util.database.prepare_sql(sql, conn)
        await statement.executemany([(
            order.order_id,
            order.product,
            order.timestamp,
            order.status.name,
            order.side,
            order.amount,
            order.price) for order in orders])


async def fetch(id: str, pool: Optional[asyncpg.Pool] = None) -> Order:
    if not pool:
        pool = quantrt.common.config.db_conn_pool
    if not pool:
        quantrt.common.log.QuantrtLog.exception("No connection pool has been configured.")
        raise EnvironmentError("No connection pool has been configured.")
    async with pool.acquire() as conn:
        sql = """
            SELECT * FROM order WHERE order_id = $1
        """
        statement = await quantrt.util.database.prepare_sql(sql, conn)
        row = await statement.fetch(id)
    return Order(
        order_id=row[0]["order_id"],
        product=row[0]["product"],
        timestamp=row[0]["timestamp"],
        status=row[0]["status"],
        side=row[0]["side"],
        amount=row[0]["amount"],
        price=row[0]["amount"]
    )


async def fetch_batch(ids: Iterator[str], pool: Optional[asyncpg.Pool] = None) -> Iterator[Order]:
    if not pool:
        pool = quantrt.common.config.db_conn_pool
    if not pool:
        quantrt.common.log.QuantrtLog.exception("No connection pool has been configured.")
        raise EnvironmentError("No connection pool has been configured.")
    async with pool.acquire() as conn:
        sql = """
            SELECT * FROM order WHERE order_id = $1
        """
        statement = await quantrt.util.database.prepare_sql(sql, conn)
        rows = [await statement.fetchrow(id) for order_id in ids]

    return [Order(
        order_id=row["order_id"],
        product=row["product"],
        timestamp=row["timestamp"],
        status=row["status"],
        side=row["side"],
        amount=row["amount"],
        price=row["amount"]
    ) for row in rows]


async def fetch_open(product_id: str, pool: Optional[asyncpg.Pool] = None) -> Iterator[Order]:
    if not pool:
        pool = quantrt.common.config.db_conn_pool
    if not pool:
        quantrt.common.log.QuantrtLog.exception("No connection pool has been configured.")
        raise EnvironmentError("No connection pool has been configured.")
    async with pool.acquire() as conn:
        sql = """
            SELECT * FROM order WHERE product = $1 AND status = "open"
        """
        statement = await quantrt.util.database.prepare_sql(sql, conn)
        rows = await statement.fetch(product_id)
    return [Order(
        order_id=row["order_id"],
        product=row["product"],
        timestamp=row["timestamp"],
        status=row["status"],
        side=row["side"],
        amount=row["amount"],
        price=row["amount"]
    ) for row in rows]
