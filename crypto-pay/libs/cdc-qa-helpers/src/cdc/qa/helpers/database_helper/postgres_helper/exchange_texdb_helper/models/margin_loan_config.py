from decimal import Decimal
from typing import List

from pydantic import Field

from . import FrozenBaseModel


class MarginLoanConfigDetail(FrozenBaseModel):
    stake_amount: int = Field(description="stake amount")
    symbol: str = Field(description="currency, e.g. CRO")
    hourly_rate: Decimal = Field(description="hourly rate")
    max_borrow_limit: Decimal = Field(description="max borrow limit")
    min_borrow_limit: Decimal = Field(description="min borrow limit")
    max_borrow_limit_5x: Decimal = Field(description="max borrow limit 5x")
    max_borrow_limit_10x: Decimal = Field(description="max borrow limit 10x")


class MarginLoanConfigList(FrozenBaseModel):
    __root__: List[MarginLoanConfigDetail] = Field(description="Margin Loan Config List")

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]
