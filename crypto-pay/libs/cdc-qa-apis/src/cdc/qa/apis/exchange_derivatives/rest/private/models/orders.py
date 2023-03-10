from typing import Any, List, Optional, Union

from cdc.qa.apis.exchange_derivatives.models import DerivativesResponse, DerivativesSignedRequest, FrozenBaseModel
from pydantic import Field, validator


class OrderDetail(FrozenBaseModel):
    account_id: str = Field(description="Account ID")
    order_id: str = Field(description="Order ID")
    client_oid: str = Field(description="Client order ID")
    order_type: str = Field(description="MARKET, LIMITD")
    time_in_force: str = Field(description="Time in force: - GOOD_TILL_CANCEL - IMMEDIATE_OR_CANCEL - FILL_OR_KILL")
    side: str = Field(description="order side: - BUY - SELL")
    exec_inst: List[str] = Field(description="- POST_ONLY (Limit Orders Only) - REDUCE_ONLY - LIQUIDATION")
    quantity: str = Field(description="Quantity specified in the order")
    limit_price: Optional[str] = Field(description="Limit price specified in the order")
    order_value: str = Field(description="Order value")
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


# private/get-open-orders
class GetOpenOrdersRequestParams(FrozenBaseModel):
    instrument_name: Optional[str] = Field(default=None, description="e.g. BTC_USDT, ETH_CRO, etc.")
    page_size: Optional[int] = Field(default=None, description="page size", ge=0, le=200)
    page: Optional[int] = Field(default=None, description="page number", ge=0)


class GetOpenOrdersRequestBody(DerivativesSignedRequest):
    method: str = "private/get-open-orders"
    params: GetOpenOrdersRequestParams = Field()


class GetOpenOrdersResult(FrozenBaseModel):
    data: List[OrderDetail] = Field()


class GetOpenOrdersResponse(DerivativesResponse):
    result: GetOpenOrdersResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/get-open-orders"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/cancel-order
class CancelOrderRequestParams(FrozenBaseModel):
    instrument_name: Optional[str] = Field(default=None, description="instrument name e.g. BTC_USDT, etc.")
    order_id: Optional[Union[int, str]] = Field(default=None, description="Optional Order ID")
    client_oid: Optional[str] = Field(default=None, description="Optional Client Order ID")


class CancelOrderRequestBody(DerivativesSignedRequest):
    method: str = "private/cancel-order"
    params: CancelOrderRequestParams = Field()


class CancelOrderResult(FrozenBaseModel):
    order_id: int = Field(description="Newly created order ID")
    client_oid: Optional[str] = Field(description="(Optional) if a Client order ID was provided in the request")


class CancelOrderResponse(DerivativesResponse):
    result: CancelOrderResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/cancel-order"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/create-order
class CreateOrderRequestParams(FrozenBaseModel):
    instrument_name: str = Field(description="instrument name e.g. BTC_USDT, etc.")
    side: str = Field(description="BUY, SELL")
    type: str = Field(description="LIMIT, MARKET, STOP_LOSS, STOP_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT")
    quantity: str = Field(
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
    price: str = Field(default=None, description="For LIMIT and STOP_LIMIT orders only: Unit price")
    post_only: bool = Field(default=False, description="POST_ONLY")
    ref_price: Optional[str] = Field(
        default=None,
        description="Trigger price required for STOP_LOSS, STOP_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT order type",
    )
    client_oid: Optional[str] = Field(description="Client Order ID")
    exec_inst: Optional[List[str]] = Field(description="POST_ONLY or MARGIN_CALL")

    def __init__(self, **data: Any):
        super().__init__(**data)
        if (
            "LIMIT" == self.type.upper()
            or "STOP_LIMIT" == self.type.upper()
            or "TAKE_PROFIT_LIMIT" == self.type.upper()
        ):
            if "LIMIT" == self.type.upper() and self.post_only is True:
                object.__setattr__(self, "exec_inst", ["POST_ONLY"])
        else:
            object.__delattr__(self, "price")
        object.__delattr__(self, "post_only")


class CreateOrderRequestBody(DerivativesSignedRequest):
    method: str = "private/create-order"
    params: CreateOrderRequestParams = Field()


class CreateOrderResult(FrozenBaseModel):
    order_id: int = Field(description="Newly created order ID")
    client_oid: Optional[str] = Field(description="(Optional) if a Client order ID was provided in the request")


class CreateOrderResponse(DerivativesResponse):
    result: Optional[CreateOrderResult] = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/create-order"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/cancel-all-orders
class CancelAllOrdersRequestParams(FrozenBaseModel):
    instrument_name: Optional[str] = Field(description="instrument name e.g. BTC_USDT, etc.")
    type: Optional[str] = Field(description="e.g. LIMIT, TRIGGER, ALL")


class CancelAllOrdersRequestBody(DerivativesSignedRequest):
    method: str = "private/cancel-all-orders"
    params: CancelAllOrdersRequestParams = Field()


class CancelAllOrdersResponse(DerivativesResponse):
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/cancel-all-orders"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/get-order-detail
class GetOrderDetailRequestParams(FrozenBaseModel):
    order_id: Union[str, int] = Field(description="order id")


class GetOrderDetailRequestBody(DerivativesSignedRequest):
    method: str = "private/get-order-detail"
    params: GetOrderDetailRequestParams = Field()


class GetOrderDetailResponse(DerivativesResponse):
    result: OrderDetail = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/get-order-detail"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/get-order-history
class GetOrderHistoryRequestParams(FrozenBaseModel):
    instrument_name: Optional[str] = Field(default=None, description="e.g. BTC_USDT, ETH_CRO, etc.")
    start_time: Optional[int] = Field(default=None, description="start timestamp", ge=0)
    end_time: Optional[int] = Field(default=None, description="start timestamp", ge=0)
    limit: Optional[int] = Field(default=None, description="page size", ge=0)


class GetOrderHistoryRequestBody(DerivativesSignedRequest):
    method: str = "private/get-order-history"
    params: GetOrderHistoryRequestParams = Field()


class GetOrderHistoryResult(FrozenBaseModel):
    data: List[OrderDetail] = Field()


class GetOrderHistoryResponse(DerivativesResponse):
    result: GetOrderHistoryResult = Field()
    method: str

    @validator("method")
    def check_method(cls, v):
        method = "private/get-order-history"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v
