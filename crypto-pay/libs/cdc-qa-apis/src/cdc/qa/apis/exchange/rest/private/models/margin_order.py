from typing import List, Optional, Union
from decimal import Decimal
from cdc.qa.apis.exchange.models import ExchangeResponse, ExchangeSignedRequest, FrozenBaseModel
from pydantic import Field

"""
include API:
private/margin/create-order
private/margin/cancel-order
private/margin/cancel-all-orders
private/margin/get-order-history
private/margin/get-open-orders
private/margin/get-order-detail
"""


# private/margin/create-order
class CreateOrderRequestParams(FrozenBaseModel):
    # https://exchange-docs.crypto.com/spot/index.html?python#private-margin-create-order
    instrument_name: str = Field(description="ETH_CRO, BTC_USDT")
    side: str = Field(description="BUY, SELL")
    type: str = Field(description="LIMIT, MARKET, STOP_LOSS, STOP_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT")
    price: Optional[Union[str, Decimal]] = Field(description="Depends For LIMIT and STOP_LIMIT orders only: Unit price")
    quantity: Optional[Union[str, Decimal]] = Field(
        description="Depends For LIMIT Orders, MARKET, STOP_LOSS, TAKE_PROFIT orders only: Order Quantity to be Sold"
    )
    notional: Optional[Union[str, Decimal]] = Field(
        description="Depends For MARKET (BUY), STOP_LOSS (BUY), TAKE_PROFIT (BUY) orders only: Amount to spend"
    )
    client_oid: Optional[str] = Field(description="Optional Client order ID")
    time_in_force: Optional[str] = Field(
        description="(Limit Orders Only) Options are: "
        "- GOOD_TILL_CANCEL (Default if unspecified)"
        "- FILL_OR_KILL "
        "- IMMEDIATE_OR_CANCEL"
    )
    exec_inst: Optional[str] = Field(description="(Limit Orders Only) Options are: - POST_ONLY - Or leave empty")
    trigger_price: Optional[Union[str, Decimal]] = Field(
        description="Used with STOP_LOSS, STOP_LIMIT, TAKE_PROFIT, and TAKE_PROFIT_LIMIT orders. "
        "Dictates when order will be triggered"
    )


class CreateOrderRequestBody(ExchangeSignedRequest):
    method: str = "private/margin/create-order"
    params: CreateOrderRequestParams


class CreateOrderResult(FrozenBaseModel):
    order_id: str = Field(description="Order id")
    client_oid: Optional[str] = Field(description="Order client oid")


class CreateOrderResponse(ExchangeResponse):
    result: Optional[CreateOrderResult] = Field()


# private/margin/cancel-order
class CancelOrderRequestParams(FrozenBaseModel):
    instrument_name: str = Field(description="instrument_name, e.g., ETH_CRO, BTC_USDT")
    order_id: str = Field(description="order id")


class CancelOrderRequestBody(ExchangeSignedRequest):
    method: str = "private/margin/cancel-order"
    params: CancelOrderRequestParams = Field(description="Cancel Order Params")


class CancelOrderResponse(ExchangeResponse):
    pass


# private/margin/cancel-all-orders
class CancelAllOrdersRequestParams(FrozenBaseModel):
    instrument_name: str = Field(description="e.g. ETH_CRO, BTC_USDT")


class CancelAllOrdersRequestBody(ExchangeSignedRequest):
    method: str = "private/margin/cancel-all-orders"
    params: CancelAllOrdersRequestParams = Field(description="Cancel all orders params")


class CancelAllOrdersResponse(ExchangeResponse):
    pass


# private/margin/get-order-history
class GetOrderHistoryRequestParams(FrozenBaseModel):
    instrument_name: Optional[str] = Field(description="e.g. ETH_CRO, BTC_USDT. Omit for 'all'")
    start_ts: Optional[int] = Field(
        description="Start timestamp (milliseconds since the Unix epoch) - defaults to 24 hours ago"
    )
    end_ts: Optional[int] = Field(description="End timestamp (milliseconds since the Unix epoch) - defaults to 'now'")
    page_size: Optional[int] = Field(description="Page size (Default: 20, max: 200)")
    page: Optional[int] = Field(description="Page number (0-based)")


class GetOrderHistoryRequestBody(ExchangeSignedRequest):
    method: str = "private/margin/get-order-history"
    params: GetOrderHistoryRequestParams = Field("Get Order history params")


class OrderDetail(FrozenBaseModel):
    status: str = Field(description="ACTIVE, CANCELED, FILLED, REJECTED or EXPIRED")
    reason: Optional[str] = Field(
        description="Reason code (see 'Response and Reason Codes') -- only for REJECTED orders"
    )
    side: str = Field(description="BUY, SELL")
    price: Decimal = Field(description="Price specified in the order")
    quantity: Decimal = Field(description="Quantity specified in the order")
    order_id: str = Field(description="Order ID")
    client_oid: str = Field(description="(Optional) Client order ID if included in request")
    create_time: int = Field(description="Order creation time (Unix timestamp)")
    update_time: int = Field(description="Order update time (Unix timestamp)")
    type: str = Field(description="LIMIT, MARKET, STOP_LOSS, STOP_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT")
    instrument_name: str = Field(description="e.g. ETH_CRO, BTC_USDT")
    cumulative_quantity: Decimal = Field(description="Cumulative executed quantity (for partially filled orders)")
    cumulative_value: Decimal = Field(description="Cumulative executed value (for partially filled orders)")
    avg_price: Decimal = Field(description="Average filled price. If none is filled, returns 0")
    fee_currency: str = Field(description="Currency used for the fees (e.g. CRO)")
    time_in_force: str = Field(description="GOOD_TILL_CANCEL, FILL_OR_KILL, IMMEDIATE_OR_CANCEL")
    exec_inst: str = Field(description="Empty or POST_ONLY (Limit Orders Only)")
    trigger_price: Optional[Decimal] = Field(description="Used for trigger-related orders")


class GetOrderHistoryResult(FrozenBaseModel):
    order_list: List[OrderDetail] = Field(description="Order list response")


class GetOrderHistoryResponse(ExchangeResponse):
    result: GetOrderHistoryResult = Field(description="Get order history result")


# private/margin/get-open-orders
class GetOpenOrdersRequestParams(FrozenBaseModel):
    instrument_name: Optional[str] = Field(description="instrument_name, e.g., ETH_CRO, BTC_USDT. Omit for 'all'")
    page_size: Optional[int] = Field(description="Page size (Default: 20, max: 200)")
    page: Optional[int] = Field(description="Page number (0-based)")


class GetOpenOrderRequestBody(ExchangeSignedRequest):
    method: str = "private/margin/get-open-orders"
    params: GetOpenOrdersRequestParams = Field(description="Get open order params")


class GetOpenOrdersResult(FrozenBaseModel):
    order_list: List[OrderDetail] = Field(description="Order list response")
    count: int = Field(description="Total count of orders")


class GetOpenOrderResponse(ExchangeResponse):
    result: GetOpenOrdersResult = Field(description="Get order history result")


# private/margin/get-order-detail
class GetOrderDetailRequestParams(FrozenBaseModel):
    order_id: str = Field(description="order id")


class GetOrderDetailRequestBody(ExchangeSignedRequest):
    method: str = "private/margin/get-order-detail"
    params: GetOrderDetailRequestParams = Field(description="Get order detail params")


class GetOrderTradeDetailInfo(FrozenBaseModel):
    side: str = Field(description="BUY, SELL")
    instrument_name: str = Field(description="e.g. ETH_CRO, BTC_USDT")
    fee: Decimal = Field(description="Trade fee")
    trade_id: str = Field(description="Trade ID")
    create_time: int = Field(description="Trade creation time")
    traded_price: Decimal = Field(description="Executed trade price")
    traded_quantity: Decimal = Field(description="Executed trade quantity")
    fee_currency: str = Field(description="Currency used for the fees (e.g. CRO)")
    order_id: str = Field(description="Order ID")
    client_oid: str = Field(description="Client OID")
    liquidity_indicator: str = Field()


class GetOrderDetailResult(FrozenBaseModel):
    trade_list: List[GetOrderTradeDetailInfo] = Field(description="Get order detail trade_list")
    order_info: OrderDetail = Field(description="Get order detail order_info")


class GetOrderDetailResponse(ExchangeResponse):
    result: GetOrderDetailResult = Field(description="Get order detail info response")
