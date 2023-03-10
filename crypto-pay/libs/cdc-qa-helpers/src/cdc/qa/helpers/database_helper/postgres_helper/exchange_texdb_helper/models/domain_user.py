from decimal import Decimal
from typing import List, Optional
from uuid import UUID

from pydantic import Field

from . import FrozenBaseModel


class DomainUserDetail(FrozenBaseModel):
    uuid: UUID = Field(description="user uuid, e.g: 00922493-31e4-497a-ba44-cac0ce8672d8")
    email: str = Field(description="email")
    is_enabled: bool
    maker_fee_discount: int = Field(description="maker_fee_discount")
    taker_fee_discount: int = Field(description="taker_fee_discount")
    user_type: str = Field(description="user type: INDIVIDUAL or RETAIL")
    two_fa_enabled: bool = Field(description="is enable two fa")
    two_fa_key: str = Field(description="two fa key")
    vip_tier: int = Field(description="VIP tier, default 1")
    margin_access: str = Field(description="DEFAULT")
    mobile_number: str = Field(description="mobile number")
    derivatives_access: str = Field(description="DEFAULT")
    lending_access: str = Field(description="DEFAULT")
    is_lending_vip: bool = Field(description="default is false")
    deriv_maker_rate_bps: Decimal = Field(description="deriv maker rate")
    deriv_taker_rate_bps: Decimal = Field(description="deriv taker rate")
    deriv_vip_tier: Optional[int] = Field(description="Deriv user tier")
    effective_vip_tier: int = Field(description="Effective Tier = max(Spot vip tier, Deriv user tier)")
    vip_tier_custom: Optional[int] = Field(description="vip tier custom")
    spot_maker_fee_discount_custom: Optional[int] = Field(description="spot maker fee discount custom")
    spot_taker_fee_discount_custom: Optional[int] = Field(description="spot taker fee discount custom")
    deriv_maker_rate_bps_custom: Optional[Decimal] = Field(description="deriv maker fee bps custom")
    deriv_taker_rate_bps_custom: Optional[Decimal] = Field(description="deriv taker fee rate bps custom")


class DomainUserList(FrozenBaseModel):
    __root__: List[DomainUserDetail] = Field(description="Domain User List")

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]
