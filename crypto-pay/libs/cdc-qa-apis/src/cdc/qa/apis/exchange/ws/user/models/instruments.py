from typing import List
from pydantic import Field, validator
from ....models import ExchangeRequest, ExchangeResponse, FrozenBaseModel


class InstrumentDetail(FrozenBaseModel):
    instrument_name: str = Field(description="e.g. BTC_USDT")
    quote_currency: str = Field(description="e.g. USDT")
    base_currency: str = Field(description="e.g. BTC")
    price_decimals: int = Field(description="Maximum decimal places for specifying price")
    quantity_decimals: int = Field(description="Maximum decimal places for specifying quantity")
    margin_trading_enabled: bool = Field(description="true or false")


class PublicGetInstrumentsRequest(ExchangeRequest):
    method = "public/get-instruments"


class PublicGetInstrumentsResponseResult(FrozenBaseModel):
    instruments: List[InstrumentDetail] = Field()


class PublicGetInstrumentsResponse(ExchangeResponse):
    result: PublicGetInstrumentsResponseResult = Field(default=None)

    @validator("method")
    def method_match(cls, v):
        assert v == "public/get-instruments", f"method expect:[public/get-instruments] actual:[{v}]!"
        return v
