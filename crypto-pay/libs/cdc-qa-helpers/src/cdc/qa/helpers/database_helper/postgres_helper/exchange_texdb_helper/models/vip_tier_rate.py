from decimal import Decimal
from typing import List
from pydantic import Field
from . import FrozenBaseModel


class VIPTierRateDetail(FrozenBaseModel):
    vip_tier: int = Field(description="vip tier")
    spot_maker_rate_pct: Decimal = Field(description="spot maker rate percent")
    spot_taker_rate_pct: Decimal = Field(description="spot taker rate percent")
    deriv_maker_rate_pct: Decimal = Field(description="Deriv maker rate percent")
    deriv_taker_rate_pct: Decimal = Field(description="Deriv taker rate percent")


class VIPTierRateList(FrozenBaseModel):
    __root__: List[VIPTierRateDetail] = Field(description="VIP Tier Rate List")

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]
