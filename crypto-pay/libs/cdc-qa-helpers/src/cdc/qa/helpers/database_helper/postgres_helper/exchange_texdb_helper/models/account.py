from decimal import Decimal
from typing import List
from uuid import UUID

from pydantic import Field

from . import FrozenBaseModel


class AccountDetail(FrozenBaseModel):
    uuid: UUID = Field(description="user uuid, e.g: 00922493-31e4-497a-ba44-cac0ce8672d8")
    maker_fee_discount: Decimal = Field(description="maker_fee_discount")
    taker_fee_discount: Decimal = Field(description="taker_fee_discount")


class AccountList(FrozenBaseModel):
    __root__: List[AccountDetail] = Field(description="account List")

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]
