from typing import NamedTuple

from .bid import Bid
from .ask import Ask


class LevelOne(NamedTuple):
    bid: Bid
    ask: Ask
