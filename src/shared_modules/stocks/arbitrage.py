from __future__ import annotations
import json
from typing import NamedTuple

from .price import Price
from .ticker import Ticker
from .exchange import Exchange
from .exchange_price import ExchangePrice


class ArbitrageOrder(NamedTuple):
    ticker: Ticker
    exchanges: LSExchanges

    def to_json(self) -> bytes:
        return json.dumps(self.to_dict()).encode("utf-8")

    def to_dict(self) -> dict:
        return {
            "ticker": self.ticker,
            "exchanges": self.exchanges.to_dict()
        }

    @staticmethod
    def from_json(data: bytes) -> ArbitrageOrder:
        parsed = json.loads(data)
        return ArbitrageOrder.from_dict(parsed)

    @staticmethod
    def from_dict(data: dict) -> ArbitrageOrder:
        return ArbitrageOrder(
            data['ticker'],
            LSExchanges.from_dict(data['exchanges'])
        )

    def __str__(self) -> str:
        return (
            f"{self.ticker}\n"
            f"\tlong : {self.exchanges.long}\n"
            f"\tshort: {self.exchanges.short}\n"
        )


class LSExchanges(NamedTuple):
    long: ExchangePrice
    short: ExchangePrice

    def to_dict(self) -> dict[str, dict[Exchange, Price]]:
        return {
            "long": self.long.to_dict(),
            "short": self.short.to_dict(),
        }

    @staticmethod
    def from_dict(data: dict) -> LSExchanges:
        return LSExchanges(
            *data['long'].values(),
            *data['short'].values(),
        )
