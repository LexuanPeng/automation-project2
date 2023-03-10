from decimal import Decimal
from typing import List, Optional, Union

from cdc.qa.apis.exchange.models import ExchangeResponse, ExchangeSignedRequest, FrozenBaseModel
from pydantic import Field, validator


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


# private/get-open-orders
class GetOpenOrdersRequestParams(FrozenBaseModel):
    instrument_name: Optional[str] = Field(default=None, description="e.g. BTC_USDT, ETH_CRO, etc.")
    page_size: Optional[int] = Field(default=None, description="page size", ge=0, le=200)
    page: Optional[int] = Field(default=None, description="page number", ge=0)


class GetOpenOrdersRequestBody(ExchangeSignedRequest):
    method: str = "private/get-open-orders"
    params: GetOpenOrdersRequestParams = Field()


class GetOpenOrdersResult(FrozenBaseModel):
    order_list: List[OrderDetail] = Field(description="Order list response")
    count: int = Field(description="Total count of orders")


class GetOpenOrdersResponse(ExchangeResponse):
    result: GetOpenOrdersResult = Field()


# private/cancel-order
class CancelOrderRequestParams(FrozenBaseModel):
    instrument_name: str = Field(default=None, description="instrument name e.g. BTC_USDT, etc.")
    order_id: str = Field(default=None, description="order ID")


class CancelOrderRequestBody(ExchangeSignedRequest):
    method: str = "private/cancel-order"
    params: CancelOrderRequestParams = Field()


class CancelOrderResponse(ExchangeResponse):
    pass


# private/create-order
class CreateOrderRequestParams(FrozenBaseModel):
    instrument_name: str = Field(description="instrument name e.g. BTC_USDT, etc.")
    side: str = Field(description="BUY, SELL")
    type: str = Field(description="LIMIT, MARKET, STOP_LOSS, STOP_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT")
    price: str = Field(default=None, description="For LIMIT and STOP_LIMIT orders only: Unit price")
    quantity: str = Field(
        description="For LIMIT Orders, MARKET (SELL), STOP_LOSS (SELL) orders only:Order Quantity to be Sold"
    )
    notional: Optional[Union[str, Decimal]] = Field(
        description="Depends For MARKET (BUY), STOP_LOSS (BUY), TAKE_PROFIT (BUY) orders only: Amount to spend"
    )
    client_oid: Optional[str] = Field(description="Optional Client order ID")
    time_in_force: Optional[str] = Field(
        description="""
        (Limit Orders Only)
        Options are:
        - GOOD_TILL_CANCEL (Default if unspecified)
        - FILL_OR_KILL
        - IMMEDIATE_OR_CANCEL"""
    )
    exec_inst: Optional[str] = Field(description="(Limit Orders Only) Options are: - POST_ONLY - Or leave empty")
    trigger_price: Optional[Union[str, Decimal]] = Field(
        description="Used with STOP_LOSS, STOP_LIMIT, TAKE_PROFIT, and TAKE_PROFIT_LIMIT orders. "
        "Dictates when order will be triggered"
    )


class CreateOrderRequestBody(ExchangeSignedRequest):
    method: str = "private/create-order"
    params: CreateOrderRequestParams = Field()


class CreateOrderResult(FrozenBaseModel):
    order_id: int = Field(description="Newly created order ID")
    client_oid: Optional[str] = Field(description="(Optional) if a Client order ID was provided in the request")


class CreateOrderResponse(ExchangeResponse):
    result: Optional[CreateOrderResult] = Field()


# private/cancel-all-orders
class CancelAllOrdersRequestParams(FrozenBaseModel):
    instrument_name: Optional[str] = Field(description="instrument name e.g. BTC_USDT, etc.")


class CancelAllOrdersRequestBody(ExchangeSignedRequest):
    method: str = "private/cancel-all-orders"
    params: CancelAllOrdersRequestParams = Field()


class CancelAllOrdersResponse(ExchangeResponse):
    pass


# private/get-order-detail
class GetOrderDetailRequestParams(FrozenBaseModel):
    order_id: str = Field(description="order id")


class GetOrderDetailRequestBody(ExchangeSignedRequest):
    method: str = "private/get-order-detail"
    params: GetOrderDetailRequestParams = Field()


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
    result: GetOrderDetailResult = Field()


# private/get-order-history
class GetOrderHistoryRequestParams(FrozenBaseModel):
    instrument_name: Optional[str] = Field(description="e.g. ETH_CRO, BTC_USDT. Omit for 'all'")
    start_ts: Optional[int] = Field(
        description="Start timestamp (milliseconds since the Unix epoch) - defaults to 24 hours ago"
    )
    end_ts: Optional[int] = Field(description="End timestamp (milliseconds since the Unix epoch) - defaults to 'now'")
    page_size: Optional[int] = Field(description="Page size (Default: 20, max: 200)")
    page: Optional[int] = Field(description="Page number (0-based)")


class GetOrderHistoryRequestBody(ExchangeSignedRequest):
    method: str = "private/get-order-history"
    params: GetOrderHistoryRequestParams = Field()


class GetOrderHistoryResult(FrozenBaseModel):
    order_list: List[OrderDetail] = Field(description="Order list response")


class GetOrderHistoryResponse(ExchangeResponse):
    result: GetOrderHistoryResult = Field()


# private/create-order-list
class CreateOrderListRequestParams(FrozenBaseModel):
    contingency_type: str = Field(description="LIST")
    order_list: List[CreateOrderRequestParams] = Field(description="CreateOrderRequestParams")


class CreateOrderListRequestBody(ExchangeSignedRequest):
    method: str = "private/create-order-list"
    params: CreateOrderListRequestParams = Field()


class ResultListDetail(FrozenBaseModel):
    index: int = Field(description="The index of corresponding order request (Start from 0)")
    code: int = Field(description="0 if success")
    message: Optional[str] = Field(description="(Optional) For server or error messages")
    order_id: str = Field(description="Newly created order ID")
    client_oid: Optional[str] = Field(
        description="(Optional) if a Client order ID was provided in the request. (Maximum 36 characters)"
    )


class CreateOrderListResult(FrozenBaseModel):
    result_list: List[ResultListDetail] = Field()


class CreateOrderListResponse(ExchangeResponse):
    result: CreateOrderListResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/create-order-list"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/cancel-order-list
class OrderListDetail(FrozenBaseModel):
    instrument_name: str = Field(description="instrument_name, e.g., ETH_CRO, BTC_USDT")
    order_id: str = Field(description="Order ID")


class CancelOrderListRequestParams(FrozenBaseModel):
    order_list: Optional[List[OrderListDetail]] = Field(
        description="For non contingency orders, A list of orders to be cancelled"
    )
    instrument_name: Optional[str] = Field(description="instrument_name")
    contingency_id: Optional[str] = Field(description="ID of the contingency order")


class CancelOrderListRequestBody(ExchangeSignedRequest):
    method: str = "private/cancel-order-list"
    params: CancelOrderListRequestParams = Field()


class CancelOrderListResponse(ExchangeResponse):
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/cancel-order-list"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v
