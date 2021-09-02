import asyncio
import base64
import hmac
import hashlib
from itertools import product
import json
import time
import websockets.client

from asyncio import Queue
from enum import Enum
from typing import Callable, Union, Dict, Optional

from src.common.types import OneOrMany, is_one
from src.common import QuantrtLog


__all__ = ["Channel", "WebsocketFeed"]


class Channel(Enum):
    Heartbeat = "heartbeat"
    Status = "status"
    Ticker = "ticker"
    Level2 = "level2"
    User = "user" # must be authenticated to use
    Matches = "matches"
    Full = "full"

    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name


class WebsocketFeed:
    """
    A class for representing the coinbasepro websocket feed api.
    """

    url: str = "wss://ws-feed.pro.coinbase.com"

    
    @property
    def connected(self) -> bool:
        return self.socket and self.socket.open


    def __init__(self, credentials: Optional[Union[str, Dict]] = None):
        # Stored credentials?
        if isinstance(credentials, str):
            with open(credentials, "r") as fhandle:
                credentials = json.load(fhandle)

        # Store credentials, if there are any, for authenticated channels
        self.credentials: Optional[Union[str, Dict]] = credentials
        # Queues of currently active subscriptions
        self.subscriptions: Dict = {}
        # Is the socket listening for messages?
        self.listening: bool = False
        # The underlying socket
        self.socket: Optional[websockets.client.WebSocketClientProtocol] = None

    
    async def on_message(self, channels: OneOrMany[Channel], product_ids: OneOrMany[str], func: Callable):

        if is_one(product_ids):
            product_ids = [product_ids]
        
        if is_one(channels):
            channels = [channels]

        channels = list(map(str, channels))

        while self.connected and self.listening:
            for channel in channels:
                if channel == "status":
                    queue: Queue =  self.subscriptions["status"]
                    message = await queue.get()
                    func(message)
                for product_id in product_ids:
                    queue: Queue = self.subscriptions[channel][product_id]
                    message = await queue.get()
                    func(message)


    async def subscribe(self, channels: OneOrMany[Channel], product_ids: OneOrMany[str]):
        request = {
            "type": "subscribe"
        }
        
        if self.credentials:
            timestamp = str(time.time())
            message = str.encode(timestamp + "get" + "/users/self/verify", encoding="utf-8")
            hmac_key = base64.b64decode(self.credentials["secret"])
            signature = hmac.new(hmac_key, message, hashlib.sha256)
            signature_b64 = signature.digest().encode('base64').rstrip('\n')

            request["CB-ACCESS-SIGN"] = signature_b64
            request["CB-ACCESS-TIMESTAMP"] = timestamp
            request["CB-ACCESS-KEY"] = self.credentials["key"]
            request["CB-ACCESS-PASSPHRASE"] = self.credentials["passphrase"]
            request["Content-Type"] = "application/json"
        
        if is_one(product_ids):
            product_ids = [product_ids]
        
        if is_one(channels):
            channels = [channels]

        channels = list(map(str, channels))

        request["product_ids"] = product_ids
        request["channels"] = channels

        if not self.connected:
            try:
                self.socket = await websockets.client.connect(self.url)
            except Exception as e:
                QuantrtLog.exception("Exception {} connecting to websocket at uri: {}".format(e, self.url))
                raise            

        message = json.dumps(request)
        await self.socket.send(message)


    async def listen(self):
        if not self.connected:
            raise AttributeError("The websocket is not currently connected")

        if self.listening:
            return

        self.listening = True

        while self.socket and self.socket.open:
            try:
                raw: str = await self.socket.recv()
                message: Dict = json.loads(raw)
                channel = message.pop("type")

                if channel == "status":
                    if "status" not in self.subscriptions:
                        self.subscriptions["status"] = Queue()
                    queue = self.subscriptions["status"]
                else:
                    product_id = message.pop("product_id")
                    if channel not in self.subscriptions:
                        self.subscriptions[channel] = {}
                    if product_id not in self.subscriptions[channel]:
                        self.subscriptions[channel][product_id] = Queue()
                    queue = self.subscriptions[channel][product_id]
                await queue.put(message)
            except Exception as e:
                QuantrtLog.exception("Exception {} trying to receive data fromt he websocket.".format(e))
                raise
        
        self.listening = False


    async def receive(self, channels: OneOrMany[Channel], product_ids: OneOrMany[str]):

        if is_one(product_ids):
            product_ids = [product_ids]

        if is_one(channels):
            channels = [channels]

        channels = list(map(str, channels))

        for channel in channels:

            if channel == "status":
                queue: Queue =  self.subscriptions["status"]
                message = await queue.get()
                yield message
                continue

            for product_id in product_ids:
                queue: Queue = self.subscriptions[channel][product_id]
                message = await queue.get()
                yield message


    async def unsubscribe(self, channels: OneOrMany[Channel], product_ids: OneOrMany[str]):
        request = {
            "type": "unsubscribe"
        }

        if is_one(product_ids):
            product_ids = [product_ids]
        
        if is_one(channels):
            channels = [channels]

        channels = list(map(str, channels))

        for channel in channels:
            if channel == "status":
                self.socket.send({})

        request["product_ids"] = product_ids
        request["channels"] = channels

        if not self.connected:
            try:
                self.socket = await websockets.client.connect(self.url)
            except Exception as e:
                QuantrtLog.exception("Exception {} connecting to websocket at uri: {}".format(e, self.url))
                raise            

        message = json.dumps(request)
        await self.socket.send(message)

        for channel in channels:
            if channel == "status":
                del self.subscriptions["status"]
                continue
            for product_id in product_ids:
                del self.subscriptions[channel][product_id]


    async def close(self):
        if not self.socket:
            return

        if not self.socket.open:
            del self.socket
            return
        
        await self.socket.close()
        del self.socket
