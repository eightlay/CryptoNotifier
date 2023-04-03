from typing import NewType, TypeAlias

Price = NewType('Price', float)
Prices: TypeAlias = list[Price]
