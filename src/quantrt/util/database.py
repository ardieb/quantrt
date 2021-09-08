import asyncpg
import asyncpg.prepared_stmt
import pandas as pd

import quantrt.common.log
import quantrt.common.config

from asyncpg import Pool


__all__ = ["create_connection_pool", "fetch_as_dataframe", "prepare_sql"]


async def create_connection_pool(dsn: str) -> Pool:
    quantrt.common.log.QuantrtLog.info("creating database connection pool")
    pool = await asyncpg.create_pool(
        dsn=dsn,
        min_size=2,
        max_size=40,
    )
    quantrt.common.log.QuantrtLog.info("database connection pool created")
    return pool


async def fetch_as_dataframe(pool: Pool, query: str, *args) -> pd.DataFrame:
    async with pool.acquire() as con:
        stmt = await con.prepare(query)
        columns = [a.name for a in stmt.get_attributes()]
        data = await stmt.fetch(*args)

        return (
            pd.DataFrame(data=data, columns=columns)
            if data and len(data) > 0
            else pd.DataFrame()
        )


async def prepare_sql(method: str, conn: asyncpg.Connection) -> asyncpg.prepared_stmt.PreparedStatement:
    if method not in quantrt.common.config.prepared_sql:
        if len(quantrt.common.config.prepared_sql) >= 32:
            quantrt.common.config.prepared_sql.popitem(last = True)
        
        statement = await conn.prepare(method)
        quantrt.common.config.prepared_sql[method] = statement

    quantrt.common.config.prepared_sql.move_to_end(method, last = False)
    return quantrt.common.config.prepared_sql[method]
