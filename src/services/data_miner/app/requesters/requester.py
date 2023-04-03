from __future__ import annotations
import os
import logging
import ccxt.async_support as ccxt
from typing import Any, TypeAlias
from ccxt.async_support.base.exchange import Exchange as ccxtExchange

from shared_modules.stocks import Ticker, Tickers, Exchange, LevelOne

ParserResponse: TypeAlias = dict[Ticker, LevelOne]
RequesterResponse: TypeAlias = tuple[Exchange, ParserResponse]


class RequesterCreator:
    @classmethod
    async def create(cls, exchange_name: Exchange) -> Requester:
        r = Requester(exchange_name)
        await r.start()
        return r


class Requester:
    def __init__(self, exchange_name: Exchange) -> None:
        self.exchange_name = exchange_name
        client = getattr(ccxt, exchange_name)
        self.client: ccxtExchange = client(self.get_settings())

    async def start(self) -> None:
        await self.client.load_markets()

    def get_settings(self) -> dict[str, Any]:
        exchange_upper = self.exchange_name.upper()
        return {
            "apiKey": os.getenv(f"{exchange_upper}_API_KEY", ''),
            "secret": os.getenv(f"{exchange_upper}_SECRET_KEY", ''),
            "enableRateLimit": True,
            "options": {
                "defaultType": "spot",
            },
        }

    async def on_stop(self) -> None:
        await self.client.close()

    async def get_level_one(self, tickers: Tickers) -> RequesterResponse:
        resp = {}

        try:
            raw_data = await self.request_level_one(tickers)
            resp = await self.parse_level_one(raw_data)
        except Exception as e:
            logging.error(e)
        finally:
            return (self.exchange_name, resp)

    async def request_level_one(self, tickers: Tickers) -> dict[str, Any]:
        if not tickers:
            return {}
        return await self.client.fetch_tickers(tickers)

    @staticmethod
    async def parse_level_one(
        data: dict[str, dict[str, Any]],
    ) -> ParserResponse:
        result: ParserResponse = {}

        for ticker, payload in data.items():
            result[ticker] = LevelOne(payload['bid'], payload['ask'])

        return result

    @property
    def markets(self):
        return self.client.markets
