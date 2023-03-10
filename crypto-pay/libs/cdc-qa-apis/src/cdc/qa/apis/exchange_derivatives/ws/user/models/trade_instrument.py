from enum import Enum
from typing import List, Optional
from pydantic import Field
from ....models import FrozenBaseModel
from ...models import SubscribeResponse, SubscribeRequest


class SubscribeUserTradeInstrumentRequestParams(FrozenBaseModel):
    channels: List[str] = Field(...)


class SubscribeUserTradeInstrumentRequest(SubscribeRequest):
    params: SubscribeUserTradeInstrumentRequestParams = Field(...)


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


class TradeInstrumentDetail(FrozenBaseModel):
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
    create_time: int = Field(description="Create timestamp in milliseconds")
    create_time_ns: int = Field(description="Create timestamp in nanoseconds")


class SubscribeUserTradeInstrumentResponseResult(FrozenBaseModel):
    instrument_name: Optional[str] = Field(description="BTCUSD-PERP")
    channel: str = Field()
    subscription: str = Field()
    data: List[TradeInstrumentDetail] = Field()


class SubscribeUserTradeInstrumentResponse(SubscribeResponse):
    result: SubscribeUserTradeInstrumentResponseResult = Field(default=None)
