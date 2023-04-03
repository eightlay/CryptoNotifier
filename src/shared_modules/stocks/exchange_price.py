from __future__ import annotations
from dataclasses import dataclass
from typing import TypeAlias

from .price import Price
from .exchange import Exchange


@dataclass
class ExchangePrice:
    exchange: Exchange
    price: Price

    def to_dict(self) -> dict[Exchange, Price]:
        return {self.exchange: self.price}

    def copy_inside(self, br: ExchangePrice) -> None:
        self.exchange = br.exchange
        self.price = br.price

    def __lt__(self, br: ExchangePrice) -> bool:
        return self.price < br.price

    def to_csv(self) -> str:
        return f"{self.exchange},{self.price}"

    def __str__(self) -> str:
        return f"{self.exchange} = {self.price}"


ExchangesPrices: TypeAlias = list[ExchangePrice]
