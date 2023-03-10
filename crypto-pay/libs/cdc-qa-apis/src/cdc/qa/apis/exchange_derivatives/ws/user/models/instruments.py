from typing import List
from pydantic import Field, validator
from ....models import DerivativesRequest, DerivativesResponse, FrozenBaseModel


class InstrumentDetail(FrozenBaseModel):
    symbol: str = Field(description="e.g BTCUSD-PERP")
    inst_type: str = Field(description="e.g PERPETUAL_SWAP")
    display_name: str = Field(description="e.g BTCUSD Perpetual")
    base_ccy: str = Field(description="e.g BTC")
    quote_ccy: str = Field(description="e.g USD_Stable_Coin")
    quote_decimals: int = Field(description="Currency decimals e.g 2", ge=0)
    quantity_decimals: int = Field(description="Currency amount e.g 4", ge=0)
    price_tick_size: str = Field(description="e.g 0.5")
    qty_tick_size: str = Field(description="e.g 0.0001")
    max_leverage: str = Field(description="Max leverage e.g 50")
    tradable: bool = Field(description="Tradable or not e.g False")


class PublicGetInstrumentsRequest(DerivativesRequest):
    method = "public/get-instruments"


class PublicGetInstrumentsResponseResult(FrozenBaseModel):
    data: List[InstrumentDetail] = Field()


class PublicGetInstrumentsResponse(DerivativesResponse):
    result: PublicGetInstrumentsResponseResult = Field(default=None)

    @validator("method")
    def method_match(cls, v):
        assert v == "public/get-instruments", f"method expect:[public/get-instruments] actual:[{v}]!"
        return v
