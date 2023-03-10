from enum import Enum
from typing import List, Optional

from cdc.qa.apis.exchange_oex.models import (
    ExchangeRequestParams,
    ExchangeResponse,
    ExchangeSignedRequest,
    FrozenBaseModel,
)
from pydantic import Field, validator


class TransactionJournalTypeEnum(Enum):
    TRADING = "TRADING"
    TRADE_FEE = "TRADE_FEE"
    WITHDRAW_FEE = "WITHDRAW_FEE"
    WITHDRAW = "WITHDRAW"
    DEPOSIT = "DEPOSIT"
    ROLLBACK_DEPOSIT = "ROLLBACK_DEPOSIT"
    ROLLBACK_WITHDRAW = "ROLLBACK_WITHDRAW"
    FUNDING = "FUNDING"
    REALIZED_PNL = "REALIZED_PNL"
    INSURANCE_FUND = "INSURANCE_FUND"
    SOCIALIZED_LOSS = "SOCIALIZED_LOSS"
    LIQUIDATION_FEE = "LIQUIDATION_FEE"
    SESSION_RESET = "SESSION_RESET"
    ADJUSTMENT = "ADJUSTMENT"
    SESSION_SETTLE = "SESSION_SETTLE"
    UNCOVERED_LOSS = "UNCOVERED_LOSS"
    ADMIN_ADJUSTMENT = "ADMIN_ADJUSTMENT"
    DELIST = "DELIST"
    SETTLEMENT_FEE = "SETTLEMENT_FEE"
    AUTO_CONVERSION = "AUTO_CONVERSION"
    MANUAL_CONVERSION = "MANUAL_CONVERSION"
    SUBACCOUNT_TX = "SUBACCOUNT_TX"
    INSURANCE_HOLD = "INSURANCE_HOLD"
    MARGIN_TRADE_INTEREST = "MARGIN_TRADE_INTEREST"


class TradeDetail(FrozenBaseModel):
    account_id: str = Field(description="Account ID")
    event_date: str = Field(description="event date")
    journal_type: TransactionJournalTypeEnum = Field(description="journal trade : TRADING")
    traded_quantity: str = Field(description="Trade quantity")
    traded_price: str = Field(description="Trade price")
    fees: str = Field(description="Trade fees, the negative sign means a deduction on balance")
    order_id: int = Field(description="Order ID")
    trade_id: int = Field(description="Trade ID")
    trade_match_id: int = Field(description="Trade match ID")
    client_oid: str = Field(description="Client Order ID")
    taker_side: str = Field(description="MAKER TAKER (empty)")
    side: str = Field(description="BUY, SELL")
    instrument_name: str = Field(description="Instrument Name")
    fee_instrument_name: str = Field(description="e.g. USD_Stable_Coin")
    create_time: int = Field(description="Create timestamp in milliseconds")
    create_time_ns: int = Field(description="Create timestamp in nanoseconds")


# private/get-trades
class GetTradesRequestParams(ExchangeRequestParams):
    instrument_name: Optional[str] = Field(default=None, description="e.g. ETH_CRO, BTC_USDT. Omit for 'all'")
    start_time: Optional[int] = Field(default=None, description="Start timestamp", ge=0)
    end_time: Optional[int] = Field(default=None, description="end timestamp", ge=0)
    limit: Optional[int] = Field(default=None, description="page limit", ge=0)


class GetTradesRequestBody(ExchangeSignedRequest):
    method: str = "private/get-trades"
    params: GetTradesRequestParams = Field()


class GetTradesResult(FrozenBaseModel):
    data: List[TradeDetail] = Field()


class GetTradesResponse(ExchangeResponse):
    result: GetTradesResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/get-trades"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/get-transactions
class TransactionDetail(FrozenBaseModel):
    account_id: str = Field(description="Account ID")
    event_date: str = Field(description="event date")
    journal_type: TransactionJournalTypeEnum = Field(description="journal trade : TRADING")
    journal_id: int = Field(description="")
    transaction_qty: str = Field(description="Transaction quantity")
    transaction_cost: str = Field(description="Transaction cost")
    realized_pnl: str = Field(description="Realized PNL")
    order_id: Optional[int] = Field(description="Order ID")
    trade_id: Optional[int] = Field(description="Trade ID")
    trade_match_id: Optional[int] = Field(description="Trade match ID")
    client_oid: str = Field(description="Client Order ID")
    taker_side: str = Field(description="MAKER TAKER (empty)")
    side: str = Field(description="BUY, SELL")
    instrument_name: str = Field(description="Instrument Name")
    event_timestamp_ms: int = Field(description="Event timestamp in milliseconds")
    event_timestamp_ns: int = Field(description="Event timestamp in nanoseconds")


class GetTransactionsRequestParams(ExchangeRequestParams):
    instrument_name: Optional[str] = Field(default=None, description="e.g. ETH_CRO, BTC_USDT. Omit for 'all'")
    journal_type: Optional[TransactionJournalTypeEnum] = Field(description="Journal type")
    start_time: Optional[int] = Field(default=None, description="Start timestamp", ge=0)
    end_time: Optional[int] = Field(default=None, description="end timestamp", ge=0)
    limit: Optional[int] = Field(default=None, description="page limit", ge=0)


class GetTransactionsRequestBody(ExchangeSignedRequest):
    method: str = "private/get-transactions"
    params: GetTransactionsRequestParams = Field()


class GetTransactionsResult(FrozenBaseModel):
    data: List[TransactionDetail] = Field()


class GetTransactionsResponse(ExchangeResponse):
    result: GetTransactionsResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/get-transactions"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/convert-collateral
class ConvertCollateralRequestParams(ExchangeRequestParams):
    client_oid: Optional[str] = Field(description="Client Order ID")
    from_instrument_name: str = Field(description="e.g. USDT")
    to_instrument_name: str = Field(description="e.g. USDC")
    from_quantity: str = Field(description="e.g. 40000")
    slippage_tolerance: Optional[str] = Field(description="e.g. 0.001000")
    floor_price: Optional[str] = Field(description="e.g. 0.999999")


class ConvertCollateralRequestBody(ExchangeSignedRequest):
    method: str = "private/convert-collateral"
    params: ConvertCollateralRequestParams = Field()


class ConvertCollateralResponse(ExchangeResponse):
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/convert-collateral"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v
