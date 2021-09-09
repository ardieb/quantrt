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
from typing import Optional, Iterable, List


@dataclass
class Account:
    # Account id from coinbase pro.
    account_id: str
    # Profile id from coinbase
    profile_id: str
    # The currency held.
    currency: str
    # How much currency is held?
    balance: Decimal
    # How much of the balance is available?
    available: Decimal
    # Is trading enabled?
    enabled: bool


async def save(account: Account, pool: Optional[asyncpg.Pool] = None):
    if not pool:
        pool = quantrt.common.config.db_conn_pool
    if not pool:
        quantrt.common.log.QuantrtLog.exception("No connection pool has been configured.")
        raise EnvironmentError("No connection pool has been configured.")

    async with pool.acquire() as conn:
        sql = """
            INSERT INTO account
                (account_id, profile_id, currency, balance, amount, enabled)
            VALUES 
                ($1, $2, $3, $4, $5, $6)
            ON CONFLICT 
                (account_id, profile_id, currency) 
            DO UPDATE
            SET 
                balance = EXCLUDED.balance,
                available = EXCLUDED.available,
                enabled = EXCLUDED.enabled
        """
        statement = await quantrt.util.database.prepare_sql(sql, conn)
        await statement.executemany((
            account.account_id,
            account.profile_id,
            account.currency,
            account.balance,
            account.available,
            account.enabled))


async def save_batch(accounts: Iterable[Account], pool: Optional[asyncpg.Pool] = None):
    if not pool:
        pool = quantrt.common.config.db_conn_pool
    if not pool:
        quantrt.common.log.QuantrtLog.exception("No connection pool has been configured.")
        raise EnvironmentError("No connection pool has been configured.")

    async with pool.acquire() as conn:
        sql = """
            INSERT INTO account
                (account_id, profile_id, currency, balance, amount, enabled)
            VALUES 
                ($1, $2, $3, $4, $5, $6)
            ON CONFLICT 
                (account_id, profile_id, currency) 
            DO UPDATE
            SET 
                balance = EXCLUDED.balance,
                available = EXCLUDED.available,
                enabled = EXCLUDED.enabled
        """
        statement = await quantrt.util.database.prepare_sql(sql, conn)
        await statement.executemany((
            account.account_id,
            account.profile_id,
            account.currency,
            account.balance,
            account.available,
            account.enabled) for account in accounts)


async def fetch(account_id: str, profile_id: str, currency: str, pool: Optional[asyncpg.Pool] = None) -> Account:
    if not pool:
        pool = quantrt.common.config.db_conn_pool
    if not pool:
        quantrt.common.log.QuantrtLog.exception("No connection pool has been configured.")
        raise EnvironmentError("No connection pool has been configured.")

    async with pool.acquire() as conn:
        sql = """
            SELECT * FROM account WHERE account_id = $1 AND profile_id = $2 AND currency = $3
        """
        statement = await quantrt.util.database.prepare_sql(sql, conn)
        row = await statement.fetchrow(account_id, profile_id, currency)
    
    return Account(
        account_id=row["account_id"],
        profile_id=row["profile_id"],
        balance=row["balance"],
        available=row["available"],
        enabled=row["enabled"]
    )


async def fetch_batch(currency: str, pool: Optional[asyncpg.Pool] = None) -> Iterable[Account]:
    if not pool:
        pool = quantrt.common.config.db_conn_pool
    if not pool:
        quantrt.common.log.QuantrtLog.exception("No connection pool has been configured.")
        raise EnvironmentError("No connection pool has been configured.")

    async with pool.acquire() as conn:
        sql = """
            SELECT * FROM account WHERE currency = $1
        """
        statement = await quantrt.util.database.prepare_sql(sql, conn)
        rows = await statement.fetch(currency)
    
    return [Account(
        account_id=row["account_id"],
        profile_id=row["profile_id"],
        balance=row["balance"],
        available=row["available"],
        enabled=row["enabled"]) for row in rows]


async def fetch_all_enabled(pool: Optional[asyncpg.Pool] = None) -> Iterable[Account]:
    if not pool:
        pool = quantrt.common.config.db_conn_pool
    if not pool:
        quantrt.common.log.QuantrtLog.exception("No connection pool has been configured.")
        raise EnvironmentError("No connection pool has been configured.")

    async with pool.acquire() as conn:
        sql = """
            SELECT * FROM account WHERE enabled = TRUE
        """
        statement = await quantrt.util.database.prepare_sql(sql, conn)
        rows = await statement.fetch()
    
    return [Account(
        account_id=row["account_id"],
        profile_id=row["profile_id"],
        balance=row["balance"],
        available=row["available"],
        enabled=row["enabled"]) for row in rows]