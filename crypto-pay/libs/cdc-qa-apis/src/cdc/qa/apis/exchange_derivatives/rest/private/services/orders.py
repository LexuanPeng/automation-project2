from typing import Union, List

from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.exchange_derivatives.rest.rest_base import DerivativesRestApi, DerivativesRestService

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
)


class GetOpenOrdersApi(DerivativesRestApi):
    """exchange deriv private gets all open orders for a particular instrument"""

    path = "private/get-open-orders"
    method = HttpMethods.POST
    request_data_type = GetOpenOrdersRequestBody
    response_type = GetOpenOrdersResponse


class CancelOrderApi(DerivativesRestApi):
    """exchange deriv private cancel an existing order"""

    path = "private/cancel-order"
    method = HttpMethods.POST
    request_data_type = CancelOrderRequestBody
    response_type = CancelOrderResponse


class CreateOrderApi(DerivativesRestApi):
    """exchange deriv private create a new BUY or SELL order"""

    path = "private/create-order"
    method = HttpMethods.POST
    request_data_type = CreateOrderRequestBody
    response_type = CreateOrderResponse


class CancelAllOrdersApi(DerivativesRestApi):
    """exchange deriv private cancels all orders for a particular instrument/pair"""

    path = "private/cancel-all-orders"
    method = HttpMethods.POST
    request_data_type = CancelAllOrdersRequestBody
    response_type = CancelAllOrdersResponse


class GetOrderDetailApi(DerivativesRestApi):
    """exchange deriv private gets Order Details for a particular order ID"""

    path = "private/get-order-detail"
    method = HttpMethods.POST
    request_data_type = GetOrderDetailRequestBody
    response_type = GetOrderDetailResponse


class GetOrderHistoryApi(DerivativesRestApi):
    """exchange deriv private gets the order history for a particular instrument"""

    path = "private/get-order-history"
    method = HttpMethods.POST
    request_data_type = GetOrderHistoryRequestBody
    response_type = GetOrderHistoryResponse


class OrderService(DerivativesRestService):
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

    def cancel_order(
        self,
        instrument_name: str = None,
        order_id: Union[str, int] = None,
        client_oid: str = None,
    ) -> CancelOrderResponse:
        """request cancel order

        Args:
            instrument_name (str, optional): instrument name. Defaults to None.
            order_id (Union[str, int], optional): order_id. Defaults to None.
            client_oid (str, optional): client_oid. Defaults to None.

        Returns:
            CancelOrderResponse: CancelOrderResponse
        """
        api = CancelOrderApi(host=self.host, _session=self.session)
        payload = CancelOrderRequestBody(
            params=CancelOrderRequestParams(instrument_name=instrument_name, order_id=order_id, client_oid=client_oid),
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
        quantity: str,
        time_in_force: str,
        price: str = None,
        post_only: bool = False,
        ref_price: str = None,
        client_oid: str = None,
        exec_inst: List[str] = None,
    ) -> CreateOrderResponse:
        """request create order
        Args:
            instrument_name (str): instrumen name
            side (str): side
            type (str): trade type
            quantity (str): quantity
            time_in_force (str): time_in_force
            price (str, optional): price, market no need price. Defaults to None.
            post_only (bool, optional): only for limit. Defaults to False.
            ref_price: only for STOP_LOSS, STOP_LIMIT, TAKE_PROFIT, TAKE_PROFIT_LIMIT
            client_oid (str, optional): Client Order ID
            exec_inst: (list, optional): POST_ONLY or MARGIN_CALL or empty
        Returns:
            response: CreateOrderResponse
        """
        api = CreateOrderApi(host=self.host, _session=self.session)
        payload = CreateOrderRequestBody(
            params=CreateOrderRequestParams(
                instrument_name=instrument_name,
                side=side,
                type=type,
                quantity=quantity,
                time_in_force=time_in_force,
                price=price,
                post_only=post_only,
                ref_price=ref_price,
                client_oid=client_oid,
                exec_inst=exec_inst,
            ),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = CreateOrderResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def cancel_all_orders(
        self,
        instrument_name: str = None,
        type: str = None,
    ) -> CancelAllOrdersResponse:
        """request cancel all orders
        Args:
            instrument_name (str, optional): instrument name. Defaults to None cancel all orders
            type (str, optional): type, e.g. LIMIT, TRIGGER, ALL. Defaults to None
        Returns:
            response: CancelAllOrdersResponse
        """
        api = CancelAllOrdersApi(host=self.host, _session=self.session)
        payload = CancelAllOrdersRequestBody(
            params=CancelAllOrdersRequestParams(instrument_name=instrument_name, type=type),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = CancelAllOrdersResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def get_order_detail(
        self,
        order_id: int,
    ) -> GetOrderDetailResponse:
        """request get order detail
        Args:
            order_id (int): order id
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
        start_time: str = None,
        end_time: str = None,
        limit: int = None,
    ) -> GetOrderHistoryResponse:
        """request get order history
        Args:
            instrument_name (str, optional): instrument name
            start_time (str, optional): start timestamp as 1622131200000000000
            end_time (str, optional): end timestamp as 1622131200000000000
            limit (int, optional): limit order count. Defaults to None.
        Returns:
            response: GetOrderHistoryResponse
        """
        api = GetOrderHistoryApi(host=self.host, _session=self.session)
        payload = GetOrderHistoryRequestBody(
            params=GetOrderHistoryRequestParams(
                instrument_name=instrument_name, start_time=start_time, end_time=end_time, limit=limit
            ),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = GetOrderHistoryResponse.parse_raw(b=api.call(data=payload).content)

        return response
