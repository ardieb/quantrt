import os

from asyncpg import Pool

from collections import OrderedDict

from quantrt.common.types import REST


__all__ = ["app_dir", "dsn", "db_conn_pool", "build_label", "rest_client", "prepared_sql"]


# The root directory of the app. This is three levels above this file's path.
app_dir: str = os.path.dirname(
    os.path.dirname(
        os.path.dirname(
            os.path.os.path.abspath(__file__))))


# The connection string for the postgres database
dsn: str = "postgresql://postgres:postgres@localhost:5432/quantrt"


# The connection pool used to connect to the postgres database.
# This is instantiated by calling database.create_connection_pool(dsn).
db_conn_pool: Pool


# This is used to identify the build when the applicaton is initialized.
build_label: str


# The global authenticated user used throughout the application lifecycle.
rest_client: REST


# SQL prepared statements for caching.
prepared_sql: OrderedDict
