from decimal import Decimal
from typing import List

from pydantic import Field

from . import FrozenBaseModel


class CurrencyDetail(FrozenBaseModel):
    symbol: str
    decimals: Decimal
    display_decimals: Decimal
    is_tradable: bool
    is_stable_coin: bool
    daily_quantity_limit: Decimal
    daily_notional_limit: Decimal


class CurrencyList(FrozenBaseModel):
    __root__: List[CurrencyDetail] = Field(description="currency List")

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]
