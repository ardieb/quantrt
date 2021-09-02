import json

from coinbasepro import AuthenticatedClient
from typing import Union, Dict


__all__ = ["authenticate_rest_client"]


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
