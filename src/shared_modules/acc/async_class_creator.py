from __future__ import annotations
from typing import Type

from .async_class_abc import AsyncClass


class ACC:
    @staticmethod
    async def create(cls_: Type[AsyncClass], *args, **kwargs):
        obj = cls_(*args, **kwargs)
        await obj.start()
        return obj
