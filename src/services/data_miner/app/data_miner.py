from __future__ import annotations
import os
import asyncio
from typing import TypeAlias
from aiokafka import AIOKafkaProducer, AIOKafkaConsumer

from shared_modules.acc import AsyncClass
from shared_modules.stocks import (
    Ticker, Tickers, Exchange, Exchanges,
    ExchangeLevelOne, ExchangesLevelsOne,
)
from shared_modules.messages import get_producer, get_consumer
from .requesters import Requesters, RequestersCreator, RequesterResponse

ParsedData: TypeAlias = dict[Ticker, ExchangesLevelsOne]


class DataMiner(AsyncClass):
    def __init__(self, exchanges: list[str]) -> None:
        self.lock = asyncio.Lock()
        self.valid_tickers: dict[Ticker, int] = {}
        self.exchanges = Exchanges.from_str_list(exchanges)
        self.tickers: dict[Exchange, set[Ticker]] = {
            e: set() for e in self.exchanges
        }
        
        self.topic_out = os.getenv("KAFKA_TOPIC_LEVEL_ONE", 'level_one')
        self.topic_in = os.getenv("KAFKA_TOPIC_SUBSCRIBE", 'subscribe')

        self.requesters: Requesters
        self.message_producer: AIOKafkaProducer
        self.message_consumer: AIOKafkaConsumer

    async def __aenter__(self) -> DataMiner:
        self.requesters = await RequestersCreator.create(self.exchanges)
        self.message_producer = await get_producer()
        self.message_consumer = await get_consumer(self.topic_in)
        return self

    async def __aexit__(self, exc_type, exc, tb) -> None:
        await self.requesters.close()
        await self.message_producer.stop()

    async def start(self) -> None:
        pass

    async def stop(self) -> None:
        pass

    async def receive_messages(self) -> None:
        tickers = Tickers()

        async for ticker in self.message_consumer:
            tickers.append(Ticker(ticker))
            
        await self.add_tickers(tickers)
        
    async def add_tickers(self, tickers: Tickers) -> None:
        async with self.lock:
            for ticker in tickers:
                await self._unsafe_add_ticker(ticker)
                
    async def _unsafe_add_ticker(self, ticker: Ticker) -> None:
        if ticker in self.valid_tickers:
            return
        
        self.valid_tickers[ticker] = len(self.exchanges)
        
        for tickers_set in self.tickers.values():
            tickers_set.add(ticker)

    async def serve_subscriptions(self) -> None:
        data = await self.get_level_one()
        
        await asyncio.gather(*(
            self.send_ticker_data(ticker, prices)
            for ticker, prices in data.items()
        ))

    async def get_level_one(self) -> ParsedData:
        async with self.lock:
            return await self._unsafe_get_level_one()

    async def _unsafe_get_level_one(self) -> ParsedData:
        result: ParsedData = {
            ticker: ExchangesLevelsOne()
            for ticker in self.valid_tickers
        }

        parsed_data: list[RequesterResponse] = await asyncio.gather(*(
            r.get_level_one(Tickers(self.tickers[e]))
            for e, r in self.requesters
        ))

        for exchange, data in parsed_data:
            for ticker, level_one in data.items():
                result[ticker].append(
                    ExchangeLevelOne(exchange, level_one)
                )

        return result

    async def send_ticker_data(
        self,
        ticker: Ticker,
        elones: ExchangesLevelsOne,
    ) -> None:
        if len(elones) == 0:
            await self.remove_ticker(ticker)
            return
        
        elones.sort_by_ask()
        
        result = []
        
        for elo in elones:
            if elo.bid == 0 or elo.ask == 0:
                await self.remove_ticker_from(ticker, elo.exchange)
            else:
                result.append(elo)

        await self.send(result)

    async def remove_ticker(self, ticker: Ticker) -> None:
        async with self.lock:
            del self.valid_tickers[ticker]

            for tckrs in self.tickers.values():
                tckrs.discard(ticker)

    async def remove_ticker_from(self, ticker: Ticker, *args: Exchange) -> None:
        async with self.lock:
            for e in set(args):
                self.valid_tickers[ticker] -= 1

                if self.valid_tickers[ticker] == 0:
                    del self.valid_tickers[ticker]

                self.tickers[e].discard(ticker)

    async def send(self, data: list[ExchangeLevelOne]) -> None:
        await self.message_producer.send(self.topic_out, data)
