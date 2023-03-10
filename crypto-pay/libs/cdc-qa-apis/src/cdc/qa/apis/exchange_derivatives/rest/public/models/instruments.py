from decimal import Decimal
from enum import Enum
from typing import List, Optional

from cdc.qa.apis.exchange_derivatives.models import DerivativesResponse, FrozenBaseModel
from pydantic import Field, validator


class InstrumentDetail(FrozenBaseModel):
    symbol: str = Field(description="e.g BTCUSD-PERP")
    inst_type: str = Field(description="e.g PERPETUAL_SWAP, WARRANT")
    display_name: str = Field(description="e.g BTCUSD Perpetual")
    base_ccy: str = Field(description="e.g BTC")
    quote_ccy: str = Field(description="e.g USD_Stable_Coin")
    quote_decimals: int = Field(description="Currency decimals e.g 2", ge=0)
    quantity_decimals: int = Field(description="Currency amount e.g 4", ge=0)
    price_tick_size: str = Field(description="e.g 0.5")
    qty_tick_size: str = Field(description="e.g 0.0001")
    max_leverage: Optional[str] = Field(description="Max leverage e.g 50")
    tradable: bool = Field(description="Tradable or not e.g False")
    beta_product: bool = Field(description="is beta product, it can be true/false")
    contract_size: Optional[str] = Field(description="contract size")
    expiry_timestamp_ms: int = Field(description="expiry timestamp ms")
    put_call: Optional[str] = Field(description="It can be PUT or CALL")
    strike: Optional[str] = Field(description="strike price")
    underlying_symbol: Optional[str] = Field(description="underlying symbol")


class InstrumentDetailV3(FrozenBaseModel):
    symbol: str = Field(description="instrument name", alias="instrument_name")
    inst_type: str = Field(description="instrument type, e.g. CCY/PERPETUAL_SWAP/FUTURE", alias="instrument_type")
    display_name: str = Field(description="display name")
    base_ccy: str = Field(description="base currency", alias="base_currency")
    quote_ccy: str = Field(description="quote currency", alias="quote_currency")
    price_decimals: int = Field(description="Currency price decimals e.g 2", ge=0)
    quantity_decimals: int = Field(description="Currency decimals e.g 2", ge=0)
    price_tick_size: str = Field(description="e.g 0.5")
    qty_tick_size: str = Field(description="e.g 0.0001", alias="quantity_tick_size")
    min_quantity: str = Field(description="min quantity, e.g. 0.00000001")
    max_leverage: Optional[str] = Field(description="max leverage")
    tradable: bool = Field(description="Tradable or not e.g False")
    expiry_timestamp_ms: int = Field(description="expiry timestamp ms")
    contract_size: Optional[str] = Field(description="contract size")
    put_call: Optional[str] = Field(description="e.g. PUT, CALL")
    strike: Optional[int] = Field(description="strike price")


class GetInstrumentsResult(FrozenBaseModel):
    data: List[InstrumentDetail] = Field()


class GetInstrumentsMethod(str, Enum):
    get_instruments = "public/get-instruments"
    get_beta_instruments = "public/get-beta-instruments"


class GetInstrumentsResponse(DerivativesResponse):
    method: GetInstrumentsMethod = Field(GetInstrumentsMethod.get_instruments)
    result: GetInstrumentsResult = Field()


class GetInstrumentsResultV3(FrozenBaseModel):
    data: List[InstrumentDetailV3] = Field()


class GetInstrumentsResponseV3(DerivativesResponse):
    method: GetInstrumentsMethod = Field(GetInstrumentsMethod.get_instruments)
    result: GetInstrumentsResultV3 = Field()


# public/get-expired-settlement-price
class GetExpiredSettlementPriceParams(FrozenBaseModel):
    instrument_type: str = Field(description="e.g. FUTURE, etc.")
    page: Optional[int] = Field(default=None, description="number")


class GetExpiredSettlementPriceResultData(FrozenBaseModel):
    i: str = Field(description="Instrument name")
    x: int = Field(description="Expiry timestamp (millisecond)")
    v: Decimal = Field(description="Value")
    t: int = Field(description="Timestamp of the data")


class GetExpiredSettlementPriceResult(FrozenBaseModel):
    data: List[GetExpiredSettlementPriceResultData] = Field(default=None)


class GetExpiredSettlementPriceResponse(DerivativesResponse):
    result: GetExpiredSettlementPriceResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "public/get-expired-settlement-price"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v
