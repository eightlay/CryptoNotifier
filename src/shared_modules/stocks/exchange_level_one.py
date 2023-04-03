from __future__ import annotations
from typing import NamedTuple

from .bid import Bid
from .ask import Ask
from .price import Price
from .exchange import Exchange
from .level_one import LevelOne


class ExchangeLevelOne(NamedTuple):
    exchange: Exchange
    level_one: LevelOne

    @property
    def bid(self) -> Bid:
        return self.level_one.bid

    @property
    def ask(self) -> Ask:
        return self.level_one.ask


class ExchangesLevelsOne(list[ExchangeLevelOne]):
    def sort_by_ask(self, ascending: bool = True) -> None:
        self.sort(key=lambda lo: lo.ask, reverse=not ascending)
