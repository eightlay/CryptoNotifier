from typing import TypeAlias

from .exchange import Exchange

Fee: TypeAlias = float
Fees: TypeAlias = dict[Exchange, Fee]
