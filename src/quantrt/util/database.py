import asyncpg
import pandas as pd

from asyncpg import Pool
from quantrt.common import QuantrtLog


async def create_connection_pool(dsn: str) -> Pool:
    QuantrtLog.info("creating database connection pool")
    pool = await asyncpg.create_pool(
        dsn=dsn,
        min_size=2,
        max_size=40,
    )
    QuantrtLog.info("database connection pool created")
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
