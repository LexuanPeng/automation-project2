from decimal import Decimal
from typing import Any, List, Optional

from pydantic import Field

from . import FrozenBaseModel


class InstrumentCurrencyMarketDetail(FrozenBaseModel):
    symbol: str = Field(description="symbol, such as BTC_USDT")
    base_currency: str = Field(description="base_currency, such as BTC")
    description: str = Field(description="BTC_USDT")
    instrument_id: int = Field(description="Instrument id")
    is_tradable: bool
    is_visible: bool
    maker_fee10th_bps: int
    max_price: Decimal
    max_quantity: Decimal
    min_maker_fee10th_bps: int
    min_price: Decimal
    min_quantity: Decimal
    min_taker_fee10th_bps: int
    price_decimals: int
    product_type: str
    quantity_decimals: int
    quote_currency: str = Field(description="quote_currency, such as USDT")
    taker_fee10th_bps: int
    cu_symbol: str
    trading_group: int
    margin_enabled: bool
    margin_enabled_5x: bool
    margin_enabled_10x: bool
    released_time: Optional[int]
    has_index_price: bool
    maker_fee_rate: Decimal = Field(default=Decimal("0.01"))
    taker_fee_rate: Decimal = Field(default=Decimal("0.01"))

    def __init__(self, **data: Any):
        super().__init__(**data)
        object.__setattr__(self, "maker_fee_rate", self.maker_fee10th_bps / Decimal("100000.0"))
        object.__setattr__(self, "taker_fee_rate", self.taker_fee10th_bps / Decimal("100000.0"))


class InstrumentCurrencyMarketList(FrozenBaseModel):
    __root__: List[InstrumentCurrencyMarketDetail] = Field(description="Instrument currency market List")

    def __iter__(self):
        return iter(self.__root__)

    def __getitem__(self, item):
        return self.__root__[item]
