import quantrt.common.config as config

from decimal import Decimal
from typing import Iterator, Optional, Union, Dict, List

from quantrt.common.log import *


__all__ = [
    "get_account", "get_accounts", "get_account_history",
    "get_account_holds", "place_order", "place_limit_order",
    "place_market_order", "cancel_order", "get_order", "get_orders",
    "get_fills", "deposit", "deposit_from_coinbase", "withdraw",
    "withdraw_to_coinbase", "withdraw_to_crypto", "get_payment_methods",
    "get_coinbase_accounts", "create_report", "get_report",
    "get_trailing_volume", "get_products", "get_product_order_book",
    "get_product_ticker", "get_product_trades", "get_product_historic_rates",
    "get_product_24hr_stats", "get_currencies", "get_time", "get_fees"
]


def submit_to_executor(func):
    async def wrapped(*args, **kwargs):
        if config.executor:
            result = await config.executor.submit(func, *args, **kwargs)
            return result
        return func(*args, **kwargs)
    return wrapped


@submit_to_executor
def get_accout(account_id: str) -> Dict:
    if not config.rest_client:
        QuantrtLog.exception(
            "Cannot submit request. Client does not exist.")
        raise EnvironmentError("Cannot submit request to coinbase. Client does not exist")
    return config.rest_client.get_account(account_id=account_id)


@submit_to_executor
def get_accounts() -> List[Dict]:
    if not config.rest_client:
        QuantrtLog.exception(
            "Cannot submit request. Client does not exist.")
        raise EnvironmentError("Cannot submit request to coinbase. Client does not exist")
    return config.rest_client.get_accounts()


@submit_to_executor
def get_account_history(account_id: str, **kwargs) -> Iterator[Dict]:
    if not config.rest_client:
        QuantrtLog.exception(
            "Cannot submit request. Client does not exist.")
        raise EnvironmentError("Cannot submit request to coinbase. Client does not exist")
    return config.rest_client.get_account_history(
        account_id=account_id, **kwargs)
    

@submit_to_executor
def get_account_holds(account_id: str, **kwargs) -> Iterator[Dict]:
    if not config.rest_client:
        QuantrtLog.exception(
            "Cannot submit request. Client does not exist.")
        raise EnvironmentError("Cannot submit request to coinbase. Client does not exist")
    return config.rest_client.get_account_holds(account_id=account_id, **kwargs)


@submit_to_executor
def place_order(
    product_id: str,
    side: str,
    order_type: str,
    stop: Optional[str] = None,
    stop_price: Optional[Union[float, Decimal]] = None,
    client_oid: Optional[str] = None,
    stp: Optional[str] = None,
    **kwargs
) -> Dict:
    if not config.rest_client:
        QuantrtLog.exception(
            "Cannot submit request. Client does not exist.")
        raise EnvironmentError("Cannot submit request to coinbase. Client does not exist")
    return config.rest_client.place_order(
        product_id=product_id,
        side=side,
        order_type=order_type,
        stop=stop,
        stop_price=stop_price,
        client_oid=client_oid,
        stp=stp,
        **kwargs
    )


@submit_to_executor
def place_limit_order(
    product_id: str,
    side: str,
    price: Union[float, Decimal],
    size: Union[float, Decimal],
    stop: Optional[str] = None,
    stop_price: Optional[Union[float, Decimal]] = None,
    client_oid: Optional[str] = None,
    stp: Optional[str] = None,
    time_in_force: Optional[str] = None,
    cancel_after: Optional[str] = None,
    post_only: Optional[bool] = None,
) -> Dict:
    if not config.rest_client:
        QuantrtLog.exception(
            "Cannot submit request. Client does not exist.")
        raise EnvironmentError("Cannot submit request to coinbase. Client does not exist")
    return config.rest_client.place_limit_order(
        product_id=product_id,
        side=side,
        price=price,
        size=size,
        stop=stop,
        stop_price=stop_price,
        client_oid=client_oid,
        stp=stp,
        time_in_force=time_in_force,
        cancel_after=cancel_after,
        post_only=post_only,
    )


@submit_to_executor
def place_market_order(
    product_id: str,
    side: str,
    size: Union[float, Decimal] = None,
    funds: Union[float, Decimal] = None,
    stop: Optional[str] = None,
    stop_price: Optional[Union[float, Decimal]] = None,
    client_oid: Optional[str] = None,
    stp: Optional[str] = None,
) -> Dict:
    if not config.rest_client:
        QuantrtLog.exception(
            "Cannot submit request. Client does not exist.")
        raise EnvironmentError("Cannot submit request to coinbase. Client does not exist")
    return config.rest_client.place_market_order(
        product_id=product_id,
        side=side,
        size=size,
        funds=funds,
        stop=stop,
        stop_price=stop_price,
        client_oid=client_oid,
        stp=stp
    )


@submit_to_executor
def cancel_order(order_id: str) -> List[str]:
    if not config.rest_client:
        QuantrtLog.exception(
            "Cannot submit request. Client does not exist.")
        raise EnvironmentError("Cannot submit request to coinbase. Client does not exist")
    return config.rest_client.cancel_order(order_id)


@submit_to_executor
def get_order(order_id: str) -> Dict:
    if not config.rest_client:
        QuantrtLog.exception(
            "Cannot submit request. Client does not exist.")
        raise EnvironmentError("Cannot submit request to coinbase. Client does not exist")
    return config.rest_client.get_order(order_id)


@submit_to_executor
def get_orders(
    product_id: Optional[str] = None,
    status: Optional[Union[str, List[str]]] = None,
    **kwargs
) -> Iterator[Dict]:
    if not config.rest_client:
        QuantrtLog.exception(
            "Cannot submit request. Client does not exist.")
        raise EnvironmentError("Cannot submit request to coinbase. Client does not exist")
    return config.rest_client.get_orders(
        product_id=product_id, status=status, **kwargs)


@submit_to_executor
def get_fills(
    product_id: Optional[str] = None, 
    order_id: Optional[str] = None, 
    **kwargs
) -> Iterator[Dict]:
    if not config.rest_client:
        QuantrtLog.exception(
            "Cannot submit request. Client does not exist.")
        raise EnvironmentError("Cannot submit request to coinbase. Client does not exist")
    return config.rest_client.get_fills(
        product_id=product_id, order_id=order_id, **kwargs)


@submit_to_executor
def deposit(
    amount: Union[float, Decimal], currency: str, payment_method_id: str
) -> Dict:
    if not config.rest_client:
        QuantrtLog.exception(
            "Cannot submit request. Client does not exist.")
        raise EnvironmentError("Cannot submit request to coinbase. Client does not exist")
    return config.rest_client.deposit(
        amount=amount, currency=currency, payment_method_id=payment_method_id
    )


@submit_to_executor
def deposit_from_coinbase(
    amount: Union[float, Decimal], currency: str, coinbase_account_id: str
) -> Dict:
    if not config.rest_client:
        QuantrtLog.exception(
            "Cannot submit request. Client does not exist.")
        raise EnvironmentError("Cannot submit request to coinbase. Client does not exist")
    return config.rest_client.deposit_from_coinbase(
        amount=amount, currency=currency, coinbase_account_id=coinbase_account_id
    )


@submit_to_executor
def withdraw(
    amount: Union[float, Decimal], currency: str, payment_method_id: str
) -> Dict:
    if not config.rest_client:
        QuantrtLog.exception(
            "Cannot submit request. Client does not exist.")
        raise EnvironmentError("Cannot submit request to coinbase. Client does not exist")
    return config.rest_client.withdraw(
        amount=amount, currency=currency, payment_method_id=payment_method_id
    )


@submit_to_executor
def withdraw_to_coinbase(
    amount: Union[float, Decimal], currency: str, coinbase_account_id: str
) -> Dict:
    if not config.rest_client:
        QuantrtLog.exception(
            "Cannot submit request. Client does not exist.")
        raise EnvironmentError("Cannot submit request to coinbase. Client does not exist")
    return config.rest_client.withdraw_to_coinbase(
        amount=amount, currency=currency, coinbase_account_id=coinbase_account_id
    )


@submit_to_executor
def withdraw_to_crypto(
    amount: Union[float, Decimal], currency: str, crypto_address: str
) -> Dict:
    if not config.rest_client:
        QuantrtLog.exception(
            "Cannot submit request. Client does not exist.")
        raise EnvironmentError("Cannot submit request to coinbase. Client does not exist")
    return config.rest_client.withdraw_to_crypto(
        amount=amount, currency=currency, crypto_address=crypto_address
    )


@submit_to_executor
def get_payment_methods() -> List[Dict]:
    if not config.rest_client:
        QuantrtLog.exception(
            "Cannot submit request. Client does not exist.")
        raise EnvironmentError("Cannot submit request to coinbase. Client does not exist")
    return config.rest_client.get_payment_methods()


@submit_to_executor
def get_coinbase_accounts() -> List[Dict]:
    if not config.rest_client:
        QuantrtLog.exception(
            "Cannot submit request. Client does not exist.")
        raise EnvironmentError("Cannot submit request to coinbase. Client does not exist")
    return config.rest_client.get_coinbase_accounts()


@submit_to_executor
def create_report(
    report_type: str,
    start_date: str,
    end_date: str,
    product_id: Optional[str] = None,
    account_id: Optional[str] = None,
    report_format: str = "pdf",
    email: Optional[str] = None,
) -> Dict:
    if not config.rest_client:
        QuantrtLog.exception(
            "Cannot submit request. Client does not exist.")
        raise EnvironmentError("Cannot submit request to coinbase. Client does not exist")
    return config.rest_client.create_report(
        report_type=report_type,
        start_date=start_date,
        end_date=end_date,
        product_id=product_id,
        account_id=account_id,
        report_format=report_format,
        email=email
    )


@submit_to_executor
def get_report(report_id: str) -> Dict:
    if not config.rest_client:
        QuantrtLog.exception(
            "Cannot submit request. Client does not exist.")
        raise EnvironmentError("Cannot submit request to coinbase. Client does not exist")
    return config.rest_client.get_report(report_id=report_id)


@submit_to_executor
def get_trailing_volume() -> List[Dict]:
    if not config.rest_client:
        QuantrtLog.exception(
            "Cannot submit request. Client does not exist.")
        raise EnvironmentError("Cannot submit request to coinbase. Client does not exist")
    return config.rest_client.get_trailing_volume()


@submit_to_executor
def get_products() -> List[Dict]:
    if not config.rest_client:
        QuantrtLog.exception(
            "Cannot submit request. Client does not exist.")
        raise EnvironmentError("Cannot submit request to coinbase. Client does not exist")
    return config.rest_client.get_products()


@submit_to_executor
def get_product_order_book(product_id: str, level: int = 1) -> Dict:
    if not config.rest_client:
        QuantrtLog.exception(
            "Cannot submit request. Client does not exist.")
        raise EnvironmentError("Cannot submit request to coinbase. Client does not exist")
    return config.rest_client.get_product_order_book(product_id=product_id, level=level)


@submit_to_executor
def get_product_ticker(product_id: str) -> Dict:
    if not config.rest_client:
        QuantrtLog.exception(
            "Cannot submit request. Client does not exist.")
        raise EnvironmentError("Cannot submit request to coinbase. Client does not exist")
    return config.rest_client.get_product_ticker(product_id=product_id)


@submit_to_executor
def get_product_trades(product_id: str, trade_id: Optional[int] = None) -> Iterator[Dict]:
    if not config.rest_client:
        QuantrtLog.exception(
            "Cannot submit request. Client does not exist.")
        raise EnvironmentError("Cannot submit request to coinbase. Client does not exist")
    return config.rest_client.get_product_trades(product_id=product_id, trade_id=trade_id)


@submit_to_executor
def get_product_historic_rates(
    product_id: str,
    start: Optional[str] = None,
    stop: Optional[str] = None,
    granularity: Optional[str] = None,
) -> List[Dict]:
    if not config.rest_client:
        QuantrtLog.exception(
            "Cannot submit request. Client does not exist.")
        raise EnvironmentError("Cannot submit request to coinbase. Client does not exist")
    return config.rest_client.get_product_historic_rates(
        product_id=product_id,
        start=start,
        stop=stop,
        granularity=granularity
    )


@submit_to_executor
def get_product_24hr_stats(product_id:str) -> Dict:
    if not config.rest_client:
        QuantrtLog.exception(
            "Cannot submit request. Client does not exist.")
        raise EnvironmentError("Cannot submit request to coinbase. Client does not exist")
    return config.rest_client.get_product_24hr_stats(product_id=product_id)


@submit_to_executor
def get_currencies() -> List[Dict]:
    if not config.rest_client:
        QuantrtLog.exception(
            "Cannot submit request. Client does not exist.")
        raise EnvironmentError("Cannot submit request to coinbase. Client does not exist")
    return config.rest_client.get_currencies()


@submit_to_executor
def get_time() -> Dict:
    if not config.rest_client:
        QuantrtLog.exception(
            "Cannot submit request. Client does not exist.")
        raise EnvironmentError("Cannot submit request to coinbase. Client does not exist")
    return config.rest_client.get_time()


@submit_to_executor
def get_fees() -> Dict:
    if not config.rest_client:
        QuantrtLog.exception(
            "Cannot submit request. Client does not exist.")
        raise EnvironmentError("Cannot submit request to coinbase. Client does not exist")
    return config.rest_client._send_message(method="GET", endpoint="/fees")
