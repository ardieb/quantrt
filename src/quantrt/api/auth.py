import base64
import hashlib
import hmac
import json
import time

import quantrt.common.log

from typing import Union, Dict


__all__ = ["load_credentials", "sign_websocket_request"]


def load_credentials(credentials: str) -> Dict:
    """Create an authenticated coinbasepro rest client api from a dictionary or json file.
    :param credentials: Either a json file with the key, secret, and passphrase or a
    dictionary mimcing this json structure.
    :return: A dictionary with the values of `secret`, `key`, and `passphrase` from the json file.
    """
    if not credentials.endswith(".json"):
        quantrt.common.log.QuantrtLog.exception(
            "The file {} is invalid. Must be a JSON file.".format(credentials))
        raise ValueError("The file {} is invalid. Must be a JSON file.".format(credentials))

    with open(credentials, "r") as fhandle:
        try:
            credentials: Dict = json.load(fhandle)
        except json.JSONDecodeError as err:
            quantrt.common.log.QuantrtLog.exception(
                "Error encountered parsing {}. {}.".format(credentials, err))
            raise err

    return {
        "key": credentials.get("key", ""),
        "secret": credentials.get("secret", ""),
        "passphrase": credentials.get("passphrase", "")
    }


def sign_websocket_request(secret: str, key: str, passphrase: str, request: Dict) -> Dict:
    """Sign a websocket request to the websocket coinbasepro feed.
    :param secret: str - the API secret.
    :param key: str - the API key.
    :param passphrase: str - the API passphrase.
    :param request: Dict - the request to sign.
    """

    timestamp = str(time.time())
    message = timestamp + "GET" + "/users/self"
    message = message.encode('ascii')
    hmac_key = base64.b64decode(secret)
    signature = hmac.new(hmac_key, message, hashlib.sha256)
    signature_b64 = base64.b64encode(signature.digest())

    request["signature"] = signature_b64.decode("ascii")
    request["key"] = key
    request["passphrase"] = passphrase
    request["timestamp"] = timestamp

    return request
