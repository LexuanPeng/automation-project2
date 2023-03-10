from typing import List, Optional
from decimal import Decimal
from cdc.qa.apis.exchange.models import ExchangeResponse, ExchangeSignedRequest, FrozenBaseModel
from pydantic import Field, StrictStr

"""
include API:
private/margin/get-interest-history
private/margin/get-liquidation-history
private/margin/get-liquidation-orders
private/margin/get-trades
"""


# private/margin/get-interest-history
class GetInterestHistoryRequestParams(FrozenBaseModel):
    currency: Optional[str] = Field(description="Currency E.g. BTC, USDT")
    start_ts: Optional[int] = Field(
        description="Default is 24 hours ago from the current timestamp. Max time range is 1 month."
    )
    end_ts: Optional[int] = Field(description="Default is current timestamp")
    page_size: Optional[int] = Field(description="Page size (Default: 20, Max: 200)")
    page: Optional[int] = Field(description="Page number (0-based)")


class GetInterestHistoryRequestBody(ExchangeSignedRequest):
    method: str = "private/margin/get-interest-history"
    params: GetInterestHistoryRequestParams = Field()


class InterestHistoryDetail(FrozenBaseModel):
    loan_id: StrictStr = Field(description="Unique identifier for the loan")
    currency: str = Field(description="Currency E.g. BTC, USDT")
    interest: Decimal = Field(description="Interest amount accrued")
    time: int = Field(description="Interest accrued time")
    stake_amount: Decimal = Field(description="Amount of CRO staked. Interest rate depends on CRO staked.")
    interest_rate: Decimal = Field(description="Hourly interest rate")


class GetInterestHistoryResult(FrozenBaseModel):
    list: List[InterestHistoryDetail] = Field("Response: Get Interest History list", alias="list")


class GetInterestHistoryResponse(ExchangeResponse):
    result: GetInterestHistoryResult = Field("Get Interest History Result")


# private/margin/get-liquidation-history
class GetLiquidationHistoryRequestParams(FrozenBaseModel):
    liquidation_status: Optional[str] = Field(
        description="Filter by whether a margin call has occurred or a liquidation event has occurred "
        "E.g. MARGIN_CALL, COMPLETED"
    )
    start_ts: Optional[int] = Field(
        description="Default is 24 hours ago from the current timestamp. Max time range is 1 month."
    )
    end_ts: Optional[int] = Field(description="Default is current timestamp")
    page_size: Optional[int] = Field(description="Page size (Default: 20, Max: 200)")
    page: Optional[int] = Field(description="Page number (0-based)")


class GetLiquidationHistoryRequestBody(ExchangeSignedRequest):
    method: str = "private/margin/get-liquidation-history"
    params: GetLiquidationHistoryRequestParams = Field()


class GetLiquidationHistoryDetail(FrozenBaseModel):
    time: int = Field(description="Event history time for a margin call or liquidation event")
    liquidation_status: str = Field(
        description="Liquidation status E.g. "
        "MARGIN_CALL is when a margin call has been issued, "
        "COMPLETED is when a liquidation event has completed"
    )
    email_status: int = Field(description="1: Email sent, otherwise email not sent")
    margin_level: str = Field(
        description="Text description of the Margin Score E.g. "
        "NORMAL means the Margin Score is > 1.30 "
        "MARGIN_CALL means 1.10 < Margin Score ≤ 1.30 "
        "LIQUIDATION means Margin Score ≤ 1.10"
    )
    message: str = Field(description="Text description of the event")
    message_code: int = Field(description="Message Code")


class GetLiquidationHistoryResult(FrozenBaseModel):
    list: List[GetLiquidationHistoryDetail]


class GetLiquidationHistoryResponse(ExchangeResponse):
    result: GetLiquidationHistoryResult


# private/margin/get-liquidation-orders
class GetLiquidationOrdersRequestParams(FrozenBaseModel):
    start_ts: Optional[int] = Field(
        description="Default is 24 hours ago from the current timestamp. Max time range is 1 month."
    )
    end_ts: Optional[int] = Field(description="Default is current timestamp")
    page_size: Optional[int] = Field(description="Page size (Default: 20, Max: 200)")
    page: Optional[int] = Field(description="Page number (0-based)")


class GetLiquidationOrdersRquestBody(ExchangeSignedRequest):
    method: str = "private/margin/get-liquidation-orders"
    params: GetLiquidationOrdersRequestParams


class GetLiquidationOrdersDetail(FrozenBaseModel):
    status: str = Field(description="ACTIVE, CANCELED, FILLED, REJECTED or EXPIRED")
    reason: Optional[str] = Field(
        description="Reason code (see 'Response and Reason Codes') -- only for REJECTED orders"
    )
    side: str = Field(description="BUY, SELL")
    price: Decimal = Field(description="Price specified in the order")
    quantity: Decimal = Field(description="Quantity specified in the order")
    order_id: str = Field(description="Order ID")
    client_oid: str = Field(description="Liquidation Order ID")
    create_time: int = Field(description="Order creation time (Unix timestamp)")
    update_time: int = Field(description="Order update time (Unix timestamp)")
    type: str = Field(description="LIMIT, MARKET")
    instrument_name: str = Field(description="e.g. BTC_USDT")
    cumulative_quantity: Decimal = Field(description="Cumulative executed quantity (for partially filled orders)")
    cumulative_value: Decimal = Field(description="Cumulative executed value (for partially filled orders)")
    avg_price: Decimal = Field(description="Average filled price. If none is filled, returns 0")
    fee_currency: str = Field(description="Currency used for the fees")
    time_in_force: str = Field(description="GOOD_TILL_CANCEL, FILL_OR_KILL, IMMEDIATE_OR_CANCEL")
    exec_inst: str = Field(description="Empty or POST_ONLY (Limit Orders Only)")


class GetLiquidationOrdersResult(FrozenBaseModel):
    order_list: List[GetLiquidationOrdersDetail]


class GetLiquidationOrdersResponse(ExchangeResponse):
    result: GetLiquidationOrdersResult


# private/margin/get-trades
class GetTradesRequestParams(FrozenBaseModel):
    instrument_name: Optional[str] = Field(description="e.g. ETH_CRO, BTC_USDT. Omit for 'all'")
    start_ts: Optional[int] = Field(
        description="Start timestamp (milliseconds since the Unix epoch) - defaults to 24 hours ago"
    )
    end_ts: Optional[int] = Field(description="End timestamp (milliseconds since the Unix epoch) - defaults to 'now'")
    page_size: Optional[int] = Field(description="Page size (Default: 20, max: 200)")
    page: Optional[int] = Field(description="Page number (0-based)")


class GetTradesRequestBody(ExchangeSignedRequest):
    method: str = "private/margin/get-trades"
    params: GetTradesRequestParams = Field(description="Get Trades Request Params")


class TradeDetailInfo(FrozenBaseModel):
    side: str = Field(description="BUY, SELL")
    instrument_name: str = Field(description="e.g. ETH_CRO, BTC_USDT")
    fee: Decimal = Field(description="Trade fee")
    trade_id: str = Field(description="Trade ID")
    create_time: int = Field(description="Trade creation time")
    traded_price: Decimal = Field(description="Executed trade price")
    traded_quantity: Decimal = Field(description="Executed trade quantity")
    fee_currency: str = Field(description="Currency used for the fees (e.g. CRO)")
    order_id: str = Field(description="Order ID")
    client_oid: str = Field(description="Client Order ID")
    liquidity_indicator: str = Field(description="TAKER or MAKER")


class GetTradesResult(FrozenBaseModel):
    trade_list: List[TradeDetailInfo] = Field(description="trade list")


class GetTradesResponse(ExchangeResponse):
    result: GetTradesResult = Field(description="Get Trade Response")
