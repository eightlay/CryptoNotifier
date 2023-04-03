from __future__ import annotations
from typing import Any, TypeAlias

Ticker: TypeAlias = str


class Tickers(list[Ticker]):
    def available_in(self, markets: dict[Ticker, Any]) -> Tickers:
        return Tickers(ticker for ticker in self if ticker in markets)
