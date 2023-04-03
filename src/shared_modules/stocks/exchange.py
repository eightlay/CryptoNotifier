from __future__ import annotations
from typing import TypeAlias


class Exchange(str):
    def lower(self) -> Exchange:
        return Exchange(super().lower())


class Exchanges(list[Exchange]):
    @staticmethod
    def from_str_list(exchanges: list[str]) -> Exchanges:
        return Exchanges(Exchange(e) for e in exchanges)
