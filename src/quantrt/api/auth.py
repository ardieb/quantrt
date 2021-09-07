import base64
import hashlib
import hmac
import json
import time

from coinbasepro import AuthenticatedClient
from typing import Union, Dict


__all__ = ["authenticate_rest_client", "sign"]


def authenticate_rest_client(credentials: Union[Dict, str]) -> AuthenticatedClient:
    """
    Create an authenticated coinbasepro rest client api from a dictionary or json file.
    :param credentials: Either a json file with the key, secret, and passphrase or a
    dictionary mimcing this json structure.
    :return: The Authenticated REST client
    """
    if isinstance(credentials, str):
            with open(credentials, "r") as fhandle:
                credentials = json.load(fhandle)
            
    return AuthenticatedClient(key=credentials["key"], 
                               secret=credentials["secret"], 
                               passphrase=credentials["passphrase"])


def sign(method: str, endpoint: str, request: Dict, credentials: Union[Dict, str]) -> Dict:

    if isinstance(credentials, str):
            with open(credentials, "r") as fhandle:
                credentials = json.load(fhandle)

    timestamp = str(time.time())
    message = str.encode(timestamp + method + endpoint, encoding="utf-8")
    hmac_key = base64.b64decode(credentials["secret"])
    signature = hmac.new(hmac_key, message, hashlib.sha256)
    signature_b64 = signature.digest()
    signature_b64 = base64.b64encode(signature_b64)

    request["CB-ACCESS-SIGN"] = signature_b64
    request["CB-ACCESS-TIMESTAMP"] = timestamp
    request["CB-ACCESS-KEY"] = credentials["key"]
    request["CB-ACCESS-PASSPHRASE"] = credentials["passphrase"]
    request["Content-Type"] = "application/json"

    return request
