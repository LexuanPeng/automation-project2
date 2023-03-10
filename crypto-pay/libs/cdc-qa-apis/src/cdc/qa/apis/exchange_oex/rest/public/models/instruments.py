from typing import List, Optional

from cdc.qa.apis.exchange_oex.models import ExchangeResponse, FrozenBaseModel
from pydantic import Field, validator


# public/get-instruments
class GetInstrumentsResultData(FrozenBaseModel):
    symbol: str = Field(description="e.g. BTCUSD-PERP")
    inst_type: str = Field(description="e.g. PERPETUAL_SWAP")
    display_name: str = Field(description="e.g. BTCUSD Perpetual")
    quote_ccy: str = Field(descirption="Quote currency, e.g. USD_Stable_Coin")
    base_ccy: str = Field(description="Base currency, e.g. BTC")
    quote_decimals: int = Field(description="Minimum decimal place for price field", ge=0)
    quantity_decimals: int = Field(description="Minimum decimal place for qty field", ge=0)
    price_tick_size: str = Field(description="Minimum price tick size")
    qty_tick_size: str = Field(description="Minimum trading quantity / tick size")
    max_leverage: str = Field(description="Max leverage of the product")
    tradable: bool = Field(description="True or False")
    expiry_timestamp_ms: int = Field(description="Expiry timestamp in millisecond")
    beta_product: Optional[bool] = Field()
    underlying_symbol: Optional[str] = Field(description="Underlying symbol")
    contract_size: Optional[str] = Field()
    margin_buy_enabled: Optional[bool] = Field()
    margin_sell_enabled: Optional[bool] = Field()
    put_call: Optional[str] = Field(description="e.g. PUT, CALL, return put_call when the instrument_type is WARRANT")
    strike: Optional[int] = Field(description="return strike price when the instrument_type is WARRANT")
    collateral_weight: Optional[str] = Field()


class GetInstrumentsResult(FrozenBaseModel):
    data: List[GetInstrumentsResultData] = Field()


class GetInstrumentsResponse(ExchangeResponse):
    method: str = "public/get-instruments"
    result: GetInstrumentsResult = Field()


class GetBetaInstrumentsResponse(ExchangeResponse):
    method: str = "public/get-beta-instruments"
    result: GetInstrumentsResult = Field()


class InstrumentDetailV3(FrozenBaseModel):
    symbol: str = Field(description="instrument name", alias="instrument_name")
    inst_type: str = Field(description="instrument type, e.g. CCY/PERPETUAL_SWAP/FUTURE", alias="instrument_type")
    instrument_type: Optional[str] = Field(
        description="instrument type, e.g. CCY/PERPETUAL_SWAP/FUTURE", alias="instrument_type"
    )
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
    underlying_instrument_name: Optional[str] = Field(
        description="return this value when instrument_type is PERPETUAL_SWAP or WARRANT"
    )
    contract_size: Optional[str] = Field(description="contract size")
    put_call: Optional[str] = Field(description="e.g. PUT, CALL, return put_call when the instrument_type is WARRANT")
    strike: Optional[int] = Field(description="return strike price when the instrument_type is WARRANT")
    margin_buy_enabled: Optional[bool] = Field(description="margin buy enabled, true/false")
    margin_sell_enabled: Optional[bool] = Field(description="margin sell enabled, true/false")


class GetInstrumentsResultV3(FrozenBaseModel):
    data: List[InstrumentDetailV3] = Field()


class GetInstrumentsResponseV3(ExchangeResponse):
    method: str = "public/get-instruments"
    result: GetInstrumentsResultV3 = Field()


class GetInstrumentsV3PathParams(FrozenBaseModel):
    instrument_type: str = Field(description="instrument type")


# public/get-expired-settlement-price
class GetExpiredSettlementPriceParams(FrozenBaseModel):
    instrument_type: str = Field(description="e.g. FUTURE, etc.")
    page: Optional[int] = Field(default=None, description="Default is 1")


class GetExpiredSettlementPriceResultData(FrozenBaseModel):
    i: str = Field(description="Instrument name")
    x: int = Field(description="Expiry timestamp (millisecond)")
    v: str = Field(description="Value")
    t: int = Field(description="Timestamp of the data")


class GetExpiredSettlementPriceResult(FrozenBaseModel):
    data: List[GetExpiredSettlementPriceResultData] = Field(default=None)


class GetExpiredSettlementPriceResponse(ExchangeResponse):
    result: GetExpiredSettlementPriceResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "public/get-expired-settlement-price"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# public/get-deposit-instruments
class GetDepositInstrumentsResponse(ExchangeResponse):
    result: List[GetInstrumentsResultData] = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "public/get-deposit-instruments"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# public/get-currencies
class GetCurrenciesResponse(ExchangeResponse):
    result: GetInstrumentsResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "public/get-currencies"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# public/get-risk-parameters
class CurrencyConfig(FrozenBaseModel):
    instrument_name: str = Field(description="Instrument name of the base currency. e.g. ETH")
    collateral_weight: Optional[str] = Field(description="Collateral weight (overrides default_max_collateral_weight)")
    max_product_leverage_for_spot: Optional[str] = Field(description="Max product leverage for Spot")
    max_product_leverage_for_perps: Optional[str] = Field(description="Max product leverage for Perpetuals")
    max_product_leverage_for_futures: Optional[str] = Field(description="Max product leverage for Futures")
    unit_margin_rate: Optional[str] = Field(description="Unit margin rate (overrides default_unit_margin_rate)")
    max_short_sell_limit: Optional[str] = Field(description="Max short sell limit")
    daily_notional_limit: Optional[str] = Field(description="Daily notional limit")
    order_limit: Optional[str] = Field(description="Order limit")


class GetRiskParametersResult(FrozenBaseModel):
    default_max_collateral_weight: str = Field(description="Default max collateral weight")
    default_max_product_leverage_for_spot: str = Field(description="Default max product leverage for Spot")
    default_max_product_leverage_for_perps: str = Field(description="Default max product leverage for Perpetuals")
    default_max_product_leverage_for_futures: str = Field(description="Default max product leverage for Futures")
    default_unit_margin_rate: str = Field(description="Default unit margin rate")
    update_timestamp_ms: str = Field(description="Update time (Unix timestamp)")
    base_currency_config: List[CurrencyConfig] = Field(description="Instrument level risk config on base currency")


class GetRiskParametersResponse(ExchangeResponse):
    result: GetRiskParametersResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "public/get-risk-parameters"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v
