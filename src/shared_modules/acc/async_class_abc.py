from __future__ import annotations
from abc import ABC, abstractmethod


class AsyncClass(ABC):
    @abstractmethod
    def __init__(self, *args, **kwargs) -> None:
        pass

    @abstractmethod
    async def __aenter__(self) -> AsyncClass:
        pass

    @abstractmethod
    async def __aexit__(self, exc_type, exc, tb) -> None:
        pass

    @abstractmethod
    async def start(self) -> None:
        pass

    @abstractmethod
    async def stop(self) -> None:
        pass
