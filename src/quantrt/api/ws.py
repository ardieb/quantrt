import json
import quantrt.api.auth

from dataclasses import dataclass
from enum import Enum
from typing import List, Dict, Optional, Tuple, Iterable
from websockets.client import WebSocketClientProtocol

from quantrt.common.types import Product


class ChannelType(Enum):
    """The channel for the websocket subscription.
    """
    # To receive heartbeat messages for specific products once a second subscribe to the heartbeat channel. 
    # Heartbeats also include sequence numbers and last trade ids that can be used to verify no messages were missed.
    Heartbeat = "heartbeat"
    # The status channel will send all products and currencies on a preset interval.
    Status = "status"
    # The ticker channel provides real-time price updates every time a match happens. 
    # It batches updates in case of cascading matches, greatly reducing bandwidth requirements.
    # Please note that more information will be added to messages from this channel in the near future.
    Ticker = "ticker"
    # The easiest way to keep a snapshot of the order book is to use the level2 channel. 
    # It guarantees delivery of all updates, which reduce a lot of the overhead required when consuming the full channel.
    # When subscribing to the channel it will send a message with the type snapshot and the corresponding product_id. 
    # Bids and asks are arrays of [price, size] tuples and represent the entire order book.
    # Subsequent updates will have the type l2update. 
    # The changes property of l2updates is an array with [side, price, size] tuples. 
    # The time property of l2update is the time of the event as recorded by our trading engine. 
    # Please note that size is the updated size at that price level, not a delta. 
    # A size of "0" indicates the price level can be removed.
    Level2 = "level2"
    # This channel is a version of the full channel that only contains messages that include the authenticated user. 
    # Consequently, you need to be authenticated to receive any messages.
    User = "user"
    # If you are only interested in match messages you can subscribe to the matches channel. 
    # This is useful when you're consuming the remaining feed using the level 2 channel.
    Matches = "matches"
    # The full channel provides real-time updates on orders and trades. 
    # These updates can be applied on to a level 3 order book snapshot to maintain an accurate and up-to-date copy of the exchange order book.
    Full = "full"


class subscription:
    """Subscription request builder.
    """
    def __init__(self):
        self.channels = []
        self.product_ids = []
        self.secret = None
        self.key = None
        self.passphrase = None
        self.type = "subscribe"
        self.has_channels = False
        self.has_products = False
    

    def to_channel(self, channel: ChannelType) -> "subscription":
        self.channels.append(channel.name)
        self.has_channels = True
        return self
    

    def to_channels(self, channels: Iterable[ChannelType]) -> "subscription":
        self.channels.extend(map(lambda channel_type: channel_type.name, channels))
        self.has_channels = True
        return self


    def to_product(self, product: Product) -> "subscription":
        self.product_ids.append(f"{product}")
        self.has_products = True
        return self


    def to_products(self, products: Iterable[Product]) -> "subscription":
        self.product_ids.extend(map(lambda product: f"{product}", products))
        self.has_products = True
        return self
    

    def to_channel_and_product(self, channel: ChannelType, product: Product) -> "subscription":
        self.channels.append({
            "name": channel.name,
            "product_ids": [f"{product}"]
        })
        self.has_channels = True
        self.has_products = True
        return self
    

    def to_channel_and_products(self, channel: ChannelType, products: Iterable[Product]) -> "subscription":
        self.channels.append({
            "name": channel.name,
            "product_ids": list(map(lambda product: f"{product}", products))
        })
        self.has_channels = True
        self.has_products = True
        return self
    

    def to_channels_and_products(self, channel_product_pairs: Iterable[Tuple[ChannelType, Iterable[Product]]]) -> "subscription":
        self.channels.extend(map(lambda pair:
            {
                "name": pair[0].name,
                "product_ids": list(map(lambda product: f"{product}", pair[1])),
            },
            channel_product_pairs,
        ))
        self.has_channels = True
        self.has_products = True
        return self


    def authenticate(self, secret: str, key: str, passphrase: str) -> "subscription":
        self.secret = secret
        self.key = key
        self.passphrase = passphrase
        return self

    
    def unsubscribe(self) -> "subscription":
        self.type = "unsubscribe"
        return self
    

    def build(self) -> str:
        if not self.has_channels:
            raise ValueError("Cannot build a subscription request without providing any channels.")

        if self.type == "subscribe" and not self.has_products:
            raise ValueError("Cannot build a subscribe request without providing any products.")

        request = {
            "type": self.type,
            "channels": self.channels,
            "product_ids": self.product_ids,
        }

        if self.secret and self.key and self.passphrase:
            quantrt.api.auth.sign_websocket_request(request)

        return json.dumps(request)
