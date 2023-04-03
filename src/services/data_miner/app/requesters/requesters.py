from __future__ import annotations
import asyncio

from shared_modules.acc import AsyncClass
from .requester import Requester, RequesterCreator
from shared_modules.stocks import Exchange, Exchanges


class Requesters(AsyncClass):
    def __init__(self, exchanges: Exchanges) -> None:
        self.requesters: dict[Exchange, Requester]
        self.exchanges = exchanges.copy()

    async def start(self) -> None:
        self.requesters = {
            r: await RequesterCreator.create(r.lower())
            for r in self.exchanges
        }

    async def stop(self):
        asyncio.gather(*(
            r.on_stop() for r in self.requesters.values()
        ))

    async def __aenter__(self) -> Requesters:
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        return

    def __iter__(self):
        return iter(self.requesters.items())

    def __getitem__(self, exchange: Exchange) -> Requester:
        return self.requesters[exchange]
