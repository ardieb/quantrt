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
    

@dataclass
class Portfolio:
    # The portfolio name in coinbase.
    name: str
    # Profile id from coinbase.
    profile_id: str
    # Trading accounts.
    accounts: List[Account]
