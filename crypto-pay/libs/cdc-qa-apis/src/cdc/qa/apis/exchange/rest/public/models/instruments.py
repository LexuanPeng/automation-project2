from decimal import Decimal
from typing import List

from cdc.qa.apis.exchange.models import ExchangeResponse, FrozenBaseModel
from pydantic import Field


class GetInstrumentsResultData(FrozenBaseModel):
    instrument_name: str = Field(description="e.g SHIB_USDT")
    quote_currency: str = Field(descirption="e.g. USDT")
    base_currency: str = Field(description="e.g. SHIB")
    price_decimals: int = Field(description="currency decimals e.g. 9", ge=0)
    quantity_decimals: int = Field(description="Currency amount e.g 4", ge=0)
    margin_trading_enabled: bool = Field(description="Margin Tradable or not e.g False")
    margin_trading_enabled_5x: bool = Field(description="Margin 5x Tradable or not e.g False")
    margin_trading_enabled_10x: bool = Field(description="Margin 10x Tradable or not e.g False")
    max_quantity: Decimal = Field(description="max_quantity")
    min_quantity: Decimal = Field(description="min_quantity")
    max_price: str = Field(description="min_quantity")
    min_price: str = Field(description="min_quantity")
    last_update_date: int = Field(description="Instrument last update time (Unix timestamp)")
    price_tick_size: str = Field(description="Price tick size")
    quantity_tick_size: str = Field(description="Quantity tick size")
    daily_trading_limit_per_base_currency: Decimal = Field(default=None)


class GetInstrumentsResult(FrozenBaseModel):
    instruments: List[GetInstrumentsResultData] = Field()


class GetInstrumentsResponse(ExchangeResponse):
    result: GetInstrumentsResult = Field()
