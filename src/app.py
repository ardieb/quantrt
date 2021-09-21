import asyncio
import argparse
import coinbasepro
import collections
import importlib.util
import json

import quantrt.api.auth as auth
import quantrt.api.rest as rest
import quantrt.common.config as config
import quantrt.util.database as dbtools
import quantrt.util.schedule as schedtools
import quantrt.util.time as timetools

from argparse import ArgumentError
from concurrent.futures import ProcessPoolExecutor
from datetime import datetime
from typing import List, Callable

from quantrt.common.types import *
from quantrt.common.log import *
from quantrt.strategy.base import *


parser = argparse.ArgumentParser()
parser.add_argument("command", type=str, choices=["backtest", "live"], action="store", dest="command",
                    help="The command to run on the app. `mine` collects market data. "
                         "`backtest` runs a backtesting strategy on stored data. "
                         "`live` runs a live strategy on realtime websocket feeds. ")
parser.add_argument("credentials", type=str, action="store", dest="credentials",
                    help="The credentials file to use to connect to Coinbase Pro. "
                         "The credentials file is a json file with the keys "
                         "`key`, `secret`, and `passphrase`.")
parser.add_argument("--start-timestamp", type=lambda s: datetime.fromisoformat(s), dest="start_tstamp", default=None,
                    help="The starting time to use for a backtester or miner in isoformat.")
parser.add_argument("--end-timestamp", type=lambda s: datetime.fromisoformat(s), dest="end_tstamp", default=datetime.now(),
                    help="The ending tme to use for a backtester or miner in isoformat. Defaults to ")
parser.add_argument("--strategy", action="extend", nargs="+", dest="strategies",
                    help="Add a `Strategy` module file to the execution runtime.")
parser.add_argument("--scrpipt", action="extend", nargs="+", dest="scripts",
                    help="Add a script to run before executing any strategies. Each scrit must have a method `main`.")


strategies: List[Strategy] = []
scripts: List[Callable] = []


async def initialize(args):
    # Label the build as `script`, `backtest`, or `live`
    config.build_label = args.command
    # Initialize curtime to be the start time from the the backtest
    if config.build_label == "backtest":
        if not args.start_timestamp:
            raise ArgumentError("User did not provide a starting timestamp required "
                             "for the the build {}".format(config.build_label))
        config.curtime = args.start_tstamp
        config.stoptime = args.end_tstamp
    
    if not args.credentials.endswith(".json"):
        raise ArgumentError("User did not provide a JSON credentials file. "
                            "Instead provided the file {}".format(args.credentials))
    # Initialize credentials
    with open(args.credentials) as fno:
        credentials = json.load(fno)
        config.api_key = credentials.get("key", "")
        config.secret_key = credentials.get("secret", "")
        config.passphrase = credentials.get("passphrase", "")

    # Create the authenticated REST client
    config.rest_client = coinbasepro.AuthenticatedClient(
        key=config.api_key, secret=config.secret_key, passphrase=config.passphrase)

    # Initialize the db connection pool
    QuantrtLog.info("Creating connection to database...")
    config.db_conn_pool = await dbtools.create_connection_pool(config.dsn)
    QuantrtLog.info("Database connection pool started.")

    # Initialize the prepared_sql statement cache
    config.prepared_sql = collections.OrderedDict()

    # Initialize the executor for submitting async requests to the api.
    config.executor = ProcessPoolExecutor()
    
    # Initialize strategies
    for name_file_pair in args.strategies:
        name, file = name_file_pair.split(":")
        spec = importlib.util.spec_from_file_location("module.name", file)
        module = importlib.util.module_from_spec(spec)
        spec.loader(module)
        CustomStrategy = getattr(module, name)
        if not issubclass(CustomStrategy, Strategy):
            raise ArgumentError("The `Strategy` {} from {} is not a subclass of `Strategy`".format(name, file))
        strategies.append(CustomStrategy(name))

    # Initialize scripts
    for file in args.scripts:
        spec = importlib.util.spec_from_file_location("module.name", file)
        module = importlib.util.module_from_spec(spec)
        spec.loader(module)
        main_func = getattr(module, "main")
        if not isinstance(main_func, Callable):
            raise ArgumentError("The `main` function of the script {} is not callable.".format(file))
        scripts.append(main_func)

    QuantrtLog.info("App resources are initialized")


async def run_scripts():
    if config.executor:
        return await asyncio.gather(*[config.executor.submit(main_func) for main_func in scripts])
    for main_func in scripts:
        main_func()
    

async def backtest():
    pass


async def live():
    pass
