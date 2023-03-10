from typing import List, Optional, Union

from cdc.qa.apis.exchange_oex.models import (
    ExchangeRequestParams,
    ExchangeResponse,
    ExchangeSignedRequest,
    FrozenBaseModel,
)
from pydantic import Field, validator


# private/get-order-detail
class OrderDetail(FrozenBaseModel):
    account_id: str = Field(description="Account ID")
    order_id: str = Field(description="Order ID")
    client_oid: str = Field(description="Client order ID")
    order_type: Optional[str] = Field(description="MARKET, LIMIT")
    time_in_force: str = Field(description="Time in force: - GOOD_TILL_CANCEL - IMMEDIATE_OR_CANCEL - FILL_OR_KILL")
    side: str = Field(description="order side: - BUY - SELL")
    exec_inst: List[str] = Field(description="- POST_ONLY (Limit Orders Only) - REDUCE_ONLY - LIQUIDATION")
    quantity: str = Field(description="Quantity specified in the order")
    limit_price: Optional[str] = Field(description="Limit price specified in the order")
    order_value: str = Field(description="Order value")
    maker_fee_rate: Optional[str] = Field(description="User's maker fee rate")
    taker_fee_rate: Optional[str] = Field(description="User's taker fee rate")
    avg_price: str = Field(description="average price")
    cumulative_quantity: str = Field(description="Cumulative executed quantity")
    cumulative_value: str = Field(description="Cumulative executed value")
    cumulative_fee: str = Field(description="Cumulative executed fee")
    status: str = Field(description="order status: NEW PENDING REJECTED ACTIVE CANCELED FILLED EXPIRED")
    update_user_id: str = Field(description="Updated user")
    order_date: str = Field(description="order creation date")
    create_time: int = Field(description="order creation timestamp")
    create_time_ns: str = Field(description="Order creation timestamp (nanosecond)")
    update_time: int = Field(description="order update timestamp")
    instrument_name: str = Field(description="Currency used for the fees")
    fee_instrument_name: str = Field(description="Currency used for the fees")
    list_id: Optional[str] = Field(description="ID of the contingency order")
    contingency_type: Optional[str] = Field(description="such as OCO")
    trigger_price: Optional[str] = Field(description="Trigger price")
    trigger_price_type: Optional[str] = Field(description="Trigger price type, such as NULL_VAL")


class GetOrderDetailRequestParams(ExchangeRequestParams):
    order_id: Optional[Union[int, str]] = Field(default=None, description="Order ID")
    client_oid: Optional[str] = Field(default=None, description="Client Order ID")


class GetOrderDetailRequestBody(ExchangeSignedRequest):
    method: str = "private/get-order-detail"
    params: GetOrderDetailRequestParams = Field()


class GetOrderDetailResponse(ExchangeResponse):
    result: OrderDetail = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/get-order-detail"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/get-open-orders
class GetOpenOrdersRequestParams(ExchangeRequestParams):
    instrument_name: Optional[str] = Field(default=None, description="e.g. BTC_USDT, ETH_CRO, etc.")


class GetOpenOrdersRequestBody(ExchangeSignedRequest):
    method: str = "private/get-open-orders"
    params: GetOpenOrdersRequestParams = Field()


class GetOpenOrdersResult(FrozenBaseModel):
    data: List[OrderDetail] = Field()


class GetOpenOrdersResponse(ExchangeResponse):
    result: GetOpenOrdersResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/get-open-orders"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/cancel-order
class CancelOrderRequestParams(ExchangeRequestParams):
    order_id: Optional[Union[int, str]] = Field(default=None, description="Optional Order ID")
    client_oid: Optional[str] = Field(default=None, description="Optional Client Order ID")


class CancelOrderRequestBody(ExchangeSignedRequest):
    method: str = "private/cancel-order"
    params: CancelOrderRequestParams = Field()


class CancelOrderResult(FrozenBaseModel):
    order_id: int = Field(description="Newly created order ID")
    client_oid: Optional[str] = Field(description="(Optional) if a Client order ID was provided in the request")


class CancelOrderResponse(ExchangeResponse):
    result: CancelOrderResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/cancel-order"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/create-order
class CreateOrderRequestParams(ExchangeRequestParams):
    instrument_name: str = Field(description="instrument name e.g. BTC_USDT, etc.")
    side: str = Field(description="BUY, SELL")
    type: str = Field(description="LIMIT, MARKET, STOP_LOSS, STOP_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT")
    quantity: Optional[str] = Field(
        description="For LIMIT Orders, MARKET (SELL), STOP_LOSS (SELL) orders only:Order Quantity to be Sold"
    )
    time_in_force: Optional[str] = Field(
        description="""
        (Limit Orders Only)
        Options are:
        - GOOD_TILL_CANCEL (Default if unspecified)
        - FILL_OR_KILL
        - IMMEDIATE_OR_CANCEL"""
    )
    price: Optional[str] = Field(default=None, description="For LIMIT and STOP_LIMIT orders only: Unit price")
    ref_price: Optional[str] = Field(
        default=None,
        description="Trigger price required for STOP_LOSS, STOP_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT order type",
    )
    client_oid: Optional[str] = Field(description="Client Order ID")
    exec_inst: Optional[List[str]] = Field(description="POST_ONLY or MARGIN_CALL")
    ref_price_type: Optional[str] = Field(
        description="which price to use for ref_price: MARK_PRICE (default), INDEX_PRICE, LAST_PRICE"
    )
    spot_margin: Optional[str] = Field(description="SPOT: non-margin order, MARGIN: margin order")
    notional: Optional[str] = Field(
        description="Apply to Spot Market Buy , Stop-Loss Market Buy, Take-Profit Market Buy order value"
    )


class CreateOrderRequestBody(ExchangeSignedRequest):
    method: str = "private/create-order"
    params: CreateOrderRequestParams = Field()


class CreateOrderResult(FrozenBaseModel):
    order_id: int = Field(description="Newly created order ID")
    client_oid: Optional[str] = Field(description="(Optional) if a Client order ID was provided in the request")


class CreateOrderResponse(ExchangeResponse):
    result: Optional[CreateOrderResult] = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/create-order"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/cancel-all-orders
class CancelAllOrdersRequestParams(ExchangeRequestParams):
    instrument_name: Optional[str] = Field(description="instrument name e.g. BTC_USDT, etc.")
    type: Optional[str] = Field(description="e.g. LIMIT, TRIGGER, ALL")


class CancelAllOrdersRequestBody(ExchangeSignedRequest):
    method: str = "private/cancel-all-orders"
    params: CancelAllOrdersRequestParams = Field()


class CancelAllOrdersResponse(ExchangeResponse):
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/cancel-all-orders"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/get-order-history
class GetOrderHistoryRequestParams(ExchangeRequestParams):
    instrument_name: Optional[str] = Field(default=None, description="e.g. BTC_USDT, ETH_CRO, etc.")
    start_time: Optional[int] = Field(default=None, description="start timestamp", ge=0)
    end_time: Optional[int] = Field(default=None, description="start timestamp", ge=0)
    limit: Optional[int] = Field(default=None, description="page size", ge=0)


class GetOrderHistoryRequestBody(ExchangeSignedRequest):
    method: str = "private/get-order-history"
    params: GetOrderHistoryRequestParams = Field()


class GetOrderHistoryResult(FrozenBaseModel):
    data: List[OrderDetail] = Field()


class GetOrderHistoryResponse(ExchangeResponse):
    result: GetOrderHistoryResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/get-order-history"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/create-order-list
class CreateOrderListRequestParams(ExchangeRequestParams):
    contingency_type: str = Field(description="OCO")
    order_list: List[CreateOrderRequestParams] = Field(description="CreateOrderRequestParams")


class CreateOrderListRequestBody(ExchangeSignedRequest):
    method: str = "private/create-order-list"
    params: CreateOrderListRequestParams = Field()


class CreateOrderListResult(FrozenBaseModel):
    list_id: int = Field()


class CreateOrderListResponse(ExchangeResponse):
    result: CreateOrderListResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/create-order-list"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/cancel-order-list
class CancelOrderListRequestParams(ExchangeRequestParams):
    contingency_type: str = Field(description="OCO")
    list_id: str = Field(description="List ID")
    instrument_name: str = Field(description="instrument_name")


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


# private/get-order-list
class GetOrderListRequestParams(ExchangeRequestParams):
    contingency_type: str = Field(description="OCO")
    list_id: str = Field(description="List ID")
    instrument_name: str = Field(description="instrument_name")


class GetOrderListRequestBody(ExchangeSignedRequest):
    method: str = "private/get-order-list"
    params: GetOrderListRequestParams = Field()


class GetOrderListResult(FrozenBaseModel):
    data: List[OrderDetail] = Field()


class GetOrderListResponse(ExchangeResponse):
    result: GetOrderListResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/get-order-list"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v
