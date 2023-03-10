from decimal import Decimal
from typing import Union, List

from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.exchange.rest.rest_base import ExchangeRestApi, ExchangeRestService

from ..models.orders import (
    CancelAllOrdersRequestBody,
    CancelAllOrdersRequestParams,
    CancelAllOrdersResponse,
    CancelOrderRequestBody,
    CancelOrderRequestParams,
    CancelOrderResponse,
    CreateOrderRequestBody,
    CreateOrderRequestParams,
    CreateOrderResponse,
    GetOpenOrdersRequestBody,
    GetOpenOrdersRequestParams,
    GetOpenOrdersResponse,
    GetOrderDetailRequestBody,
    GetOrderDetailRequestParams,
    GetOrderDetailResponse,
    GetOrderHistoryRequestBody,
    GetOrderHistoryRequestParams,
    GetOrderHistoryResponse,
    CreateOrderListRequestBody,
    CreateOrderListRequestParams,
    CreateOrderListResponse,
    CancelOrderListRequestBody,
    CancelOrderListResponse,
    CancelOrderListRequestParams,
)


class GetOpenOrdersApi(ExchangeRestApi):
    """exchange-private gets all open orders for a particular instrument"""

    path = "private/get-open-orders"
    method = HttpMethods.POST
    request_data_type = GetOpenOrdersRequestBody
    response_type = GetOpenOrdersResponse


class CancelOrderApi(ExchangeRestApi):
    """exchange-private cancel an existing order"""

    path = "private/cancel-order"
    method = HttpMethods.POST
    request_data_type = CancelOrderRequestBody
    response_type = CancelOrderResponse


class CreateOrderApi(ExchangeRestApi):
    """exchange-private create a new BUY or SELL order"""

    path = "private/create-order"
    method = HttpMethods.POST
    request_data_type = CreateOrderRequestBody
    response_type = CreateOrderResponse


class CancelAllOrdersApi(ExchangeRestApi):
    """exchange-private cancels all orders for a particular instrument/pair"""

    path = "private/cancel-all-orders"
    method = HttpMethods.POST
    request_data_type = CancelAllOrdersRequestBody
    response_type = CancelAllOrdersResponse


class GetOrderDetailApi(ExchangeRestApi):
    """exchange-private gets Order Details for a particular order ID"""

    path = "private/get-order-detail"
    method = HttpMethods.POST
    request_data_type = GetOrderDetailRequestBody
    response_type = GetOrderDetailResponse


class GetOrderHistoryApi(ExchangeRestApi):
    """exchange-private gets the order history for a particular instrument"""

    path = "private/get-order-history"
    method = HttpMethods.POST
    request_data_type = GetOrderHistoryRequestBody
    response_type = GetOrderHistoryResponse


class CreateOrderListApi(ExchangeRestApi):
    """exchange private create order list"""

    path = "private/create-order-list"
    method = HttpMethods.POST
    request_data_type = CreateOrderListRequestBody
    response_type = CreateOrderListResponse


class CancelOrderListApi(ExchangeRestApi):
    """exchange private create order list"""

    path = "private/cancel-order-list"
    method = HttpMethods.POST
    request_data_type = CancelOrderListRequestBody
    response_type = CancelOrderListResponse


class OrderService(ExchangeRestService):
    def get_open_orders(
        self,
        instrument_name: str = None,
        page_size: int = None,
        page: int = None,
    ) -> GetOpenOrdersResponse:
        """request get open orders
        Args:
            instrument_name (str, optional): instrument name, None for allow. Defaults to None.
            page_size (int, optional): page size. Defaults to 20.
            page (int, optional): page number, 0 based. Defaults to 0.
        Returns:
            response: GetOpenOrdersResponse
        """
        api = GetOpenOrdersApi(host=self.host, _session=self.session)
        payload = GetOpenOrdersRequestBody(
            params=GetOpenOrdersRequestParams(instrument_name=instrument_name, page_size=page_size, page=page),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = GetOpenOrdersResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def cancel_order(self, instrument_name: str, order_id: str) -> CancelOrderResponse:
        """request cancel order
        Args:
            instrument_name (str): instrument name
            order_id (str): order_id
        Returns:
            response: CancelOrderResponse
        """
        api = CancelOrderApi(host=self.host, _session=self.session)
        payload = CancelOrderRequestBody(
            params=CancelOrderRequestParams(instrument_name=instrument_name, order_id=order_id),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = CancelOrderResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def create_order(
        self,
        instrument_name: str,
        side: str,
        type: str,
        price: Union[str, Decimal] = None,
        quantity: Union[str, Decimal] = None,
        notional: Union[str, Decimal] = None,
        client_oid: str = None,
        time_in_force: str = None,
        exec_inst: str = None,
        trigger_price: Union[str, Decimal] = None,
    ) -> CreateOrderResponse:
        """
        request private/margin/create-order
        Args:
            instrument_name: e.g., ETH_CRO, BTC_USDT
            side: BUY, SELL
            type: LIMIT, MARKET, STOP_LOSS, STOP_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT
            price: For LIMIT and STOP_LIMIT orders only: Unit price
            quantity: For LIMIT Orders, MARKET, STOP_LOSS, TAKE_PROFIT orders only: Order Quantity to be Sold
            notional: For MARKET (BUY), STOP_LOSS (BUY), TAKE_PROFIT (BUY) orders only: Amount to spend
            client_oid: Optional Client order ID
            time_in_force: (Limit Orders Only) ptions are: GOOD_TILL_CANCEL (Default if unspecified),
                            FILL_OR_KILL, IMMEDIATE_OR_CANCEL
            exec_inst: (Limit Orders Only) Options are: POST_ONLY Or leave empty
            trigger_price: Used with STOP_LOSS, STOP_LIMIT, TAKE_PROFIT, and TAKE_PROFIT_LIMIT orders.
                            Dictates when order will be triggered

        Returns:
            CreateOrderResponse
        """
        api = CreateOrderApi(host=self.host, _session=self.session)
        params = {
            "instrument_name": instrument_name,
            "side": side,
            "type": type,
            "price": price,
            "quantity": quantity,
            "notional": notional,
            "client_oid": client_oid,
            "time_in_force": time_in_force,
            "exec_inst": exec_inst,
            "trigger_price": trigger_price,
        }
        payload = CreateOrderRequestBody(
            params=CreateOrderRequestParams(**params), api_key=self.api_key, secret_key=self.secret_key
        ).json(exclude_none=True)
        response = CreateOrderResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def cancel_all_orders(
        self,
        instrument_name: str = None,
    ) -> CancelAllOrdersResponse:
        """request cancel all orders
        Args:
            instrument_name (str, optional): instrument name. Defaults to None cancel all orders
        Returns:
            response: CancelAllOrdersResponse
        """
        api = CancelAllOrdersApi(host=self.host, _session=self.session)
        payload = CancelAllOrdersRequestBody(
            params=CancelAllOrdersRequestParams(instrument_name=instrument_name),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = CancelAllOrdersResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def get_order_detail(
        self,
        order_id: str,
    ) -> GetOrderDetailResponse:
        """request get order detail
        Args:
            order_id (str): order id
        Returns:
            response: GetOrderDetailResponse
        """
        api = GetOrderDetailApi(host=self.host, _session=self.session)
        payload = GetOrderDetailRequestBody(
            params=GetOrderDetailRequestParams(order_id=order_id),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = GetOrderDetailResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def get_order_history(
        self,
        instrument_name: str = None,
        start_ts: int = None,
        end_ts: int = None,
        page_size: int = None,
        page: int = None,
    ) -> GetOrderHistoryResponse:
        """request get order history
        Args:
            instrument_name: e.g. ETH_CRO, BTC_USDT. Omit for 'all'
            strart_ts: Start timestamp (milliseconds since the Unix epoch) - defaults to 24 hours ago
            end_ts: End timestamp (milliseconds since the Unix epoch) - defaults to 'now'
            page_size: Page size (Default: 20, max: 200)
            page: Page number (0-based)

        Returns:
            response: GetOrderHistoryResponse
        """
        params = {
            "instrument_name": instrument_name,
            "start_ts": start_ts,
            "end_ts": end_ts,
            "page_size": page_size,
            "page": page,
        }
        api = GetOrderHistoryApi(host=self.host, _session=self.session)
        payload = GetOrderHistoryRequestBody(
            params=GetOrderHistoryRequestParams(**params), api_key=self.api_key, secret_key=self.secret_key
        ).json(exclude_none=True)
        response = GetOrderHistoryResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def create_order_list(
        self,
        contingency_type: str,
        order_list: List[CreateOrderRequestParams],
    ) -> CreateOrderListResponse:
        """request create order list
        Args:
            contingency_type (str): OCO
            order_list (list): Exactly 2 orders
            system_label:

        Returns:
            response: CreateOrderListResponse
        """
        api = CreateOrderListApi(host=self.host, _session=self.session)
        payload = CreateOrderListRequestBody(
            params=CreateOrderListRequestParams(
                contingency_type=contingency_type,
                order_list=order_list,
            ),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = CreateOrderListResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def cancel_order_list(
        self,
        order_list: list = None,
        instrument_name: str = None,
        contingency_id: str = None,
    ) -> CancelOrderListResponse:
        """request cancel order list
        Args:
            order_list (str): For non contingency orders, A list of orders to be cancelled
            instrument_name (str): instrument name
            contingency_id (str): ID of the contingency order
        Returns:
            response: CancelOrderListResponse
        """
        api = CancelOrderListApi(host=self.host, _session=self.session)
        payload = CancelOrderListRequestBody(
            params=CancelOrderListRequestParams(
                order_list=order_list,
                instrument_name=instrument_name,
                contingency_id=contingency_id,
            ),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = CancelOrderListResponse.parse_raw(b=api.call(data=payload).content)

        return response
