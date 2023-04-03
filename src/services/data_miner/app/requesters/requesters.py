from __future__ import annotations
import asyncio

from .requester import Requester, RequesterCreator
from shared_modules.stocks import Exchange, Exchanges


class RequestersCreator:
    @classmethod
    async def create(cls, exchanges: Exchanges) -> Requesters:
        r = Requesters(exchanges)
        await r.start()
        return r


class Requesters:
    def __init__(self, exchanges: Exchanges) -> None:
        self.requesters: dict[Exchange, Requester]
        self.exchanges = exchanges.copy()

    async def start(self) -> None:
        self.requesters = {
            r: await RequesterCreator.create(r.lower())
            for r in self.exchanges
        }

    async def close(self):
        asyncio.gather(*(
            r.on_stop() for r in self.requesters.values()
        ))

    def __iter__(self):
        return iter(self.requesters.items())

    def __getitem__(self, exchange: Exchange) -> Requester:
        return self.requesters[exchange]
