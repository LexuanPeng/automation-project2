from decimal import Decimal
from typing import Union

from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.exchange.rest.rest_base import ExchangeRestApi, ExchangeRestService

from ..models.margin_account import (
    TransferResponse,
    TransferRequestBody,
    BorrowResponse,
    GetTransferHistoryResponse,
    GetRepayHistoryRequestParams,
    GetTransferHistoryRequestBody,
    GetUserConfigRequestBody,
    GetUserConfigResponse,
    RepayResponse,
    GetBorrowHistoryRequestParams,
    GetAccountSummaryResponse,
    GetRepayHistoryRequestBody,
    GetRepayHistoryResponse,
    BorrowRequestBody,
    RepayRequestBody,
    GetBorrowHistoryRequestBody,
    GetBorrowHistoryResponse,
    GetAccountSummaryRequestBody,
    RepayRequestParams,
    BorrowRequestParams,
    TransferRequestParams,
    GetTransferHistoryRequestParams,
    AdjustMarginLeverageRequestParams,
    AdjustMarginLeverageRequestBody,
    AdjustMarginLeverageResponse,
    GetMarginTradingUserRequestBody,
    GetMarginTradingUserResponse,
)
from ..models.margin_trade import (
    GetLiquidationOrdersRequestParams,
    GetLiquidationOrdersRquestBody,
    GetLiquidationOrdersResponse,
    GetLiquidationHistoryRequestParams,
    GetLiquidationHistoryRequestBody,
    GetLiquidationHistoryResponse,
    GetInterestHistoryRequestBody,
    GetInterestHistoryRequestParams,
    GetInterestHistoryResponse,
    GetTradesRequestParams,
    GetTradesRequestBody,
    GetTradesResponse,
)
from ..models.margin_order import (
    CreateOrderRequestParams,
    CreateOrderResponse,
    CreateOrderRequestBody,
    CancelOrderRequestParams,
    CancelOrderRequestBody,
    CancelOrderResponse,
    CancelAllOrdersRequestParams,
    CancelAllOrdersRequestBody,
    CancelAllOrdersResponse,
    GetOrderHistoryRequestParams,
    GetOrderHistoryRequestBody,
    GetOrderHistoryResponse,
    GetOpenOrdersRequestParams,
    GetOpenOrderRequestBody,
    GetOpenOrderResponse,
    GetOrderDetailRequestParams,
    GetOrderDetailRequestBody,
    GetOrderDetailResponse,
)


class TransferApi(ExchangeRestApi):
    """Transfers funds between spot and margin wallet."""

    path = "private/margin/transfer"
    method = HttpMethods.POST
    request_data_type = TransferRequestBody
    response_type = TransferResponse


class GetTransferHistoryApi(ExchangeRestApi):
    """Get the transfer history between the Spot and Margin Wallet."""

    path = "private/margin/get-transfer-history"
    method = HttpMethods.POST
    request_data_type = GetTransferHistoryRequestBody
    response_type = GetTransferHistoryResponse


class GetUserConfigApi(ExchangeRestApi):
    path = "private/margin/get-user-config"
    method = HttpMethods.POST
    request_params_type = GetUserConfigRequestBody
    response_type = GetUserConfigResponse


class GetAccountSummaryApi(ExchangeRestApi):
    path = "private/margin/get-account-summary"
    method = HttpMethods.POST
    request_params_type = GetAccountSummaryRequestBody
    response_type = GetAccountSummaryResponse


class BorrowApi(ExchangeRestApi):
    path = "private/margin/borrow"
    method = HttpMethods.POST
    request_params_type = BorrowRequestBody
    response_type = BorrowResponse


class RepayApi(ExchangeRestApi):
    path = "private/margin/repay"
    method = HttpMethods.POST
    request_params_type = RepayRequestBody
    response_type = RepayResponse


class GetBorrowHistoryApi(ExchangeRestApi):
    path = "private/margin/get-borrow-history"
    method = HttpMethods.POST
    request_params_type = GetBorrowHistoryRequestBody
    response_type = GetBorrowHistoryResponse


class GetInterestHistoryApi(ExchangeRestApi):
    path = "private/margin/get-interest-history"
    method = HttpMethods.POST
    request_params_type = GetInterestHistoryRequestBody
    response_type = GetInterestHistoryResponse


class GetRepayHistoryApi(ExchangeRestApi):
    path = "private/margin/get-repay-history"
    method = HttpMethods.POST
    request_params_type = GetRepayHistoryRequestBody
    response_type = GetRepayHistoryResponse


class GetLiquidationHistoryApi(ExchangeRestApi):
    path = "private/margin/get-liquidation-history"
    method = HttpMethods.POST
    request_params_type = GetLiquidationHistoryRequestBody
    response_type = GetLiquidationHistoryResponse


class GetLiquidationOrdersApi(ExchangeRestApi):
    path = "private/margin/get-liquidation-orders"
    method = HttpMethods.POST
    request_params_type = GetLiquidationOrdersRquestBody
    response_type = GetLiquidationOrdersResponse


class CreateOrderApi(ExchangeRestApi):
    path = "private/margin/create-order"
    method = HttpMethods.POST
    request_params_type = CreateOrderRequestBody
    response_type = CreateOrderResponse


class CancelOrderApi(ExchangeRestApi):
    path = "private/margin/cancel-order"
    method = HttpMethods.POST
    request_params_type = CancelOrderRequestBody
    response_type = CancelOrderResponse


class CancelAllOrdersApi(ExchangeRestApi):
    path = "private/margin/cancel-all-orders"
    method = HttpMethods.POST
    request_params_type = CancelAllOrdersRequestBody
    response_type = CancelAllOrdersResponse


class GetOrderHistoryApi(ExchangeRestApi):
    path = "private/margin/get-order-history"
    method = HttpMethods.POST
    request_params_type = GetOrderHistoryRequestBody
    response_type = GetOrderHistoryResponse


class GetOpenOrdersApi(ExchangeRestApi):
    path = "private/margin/get-open-orders"
    method = HttpMethods.POST
    request_params_type = GetOpenOrderRequestBody
    response_type = GetOpenOrderResponse


class GetOrderDetailApi(ExchangeRestApi):
    path = "private/margin/get-order-detail"
    method = HttpMethods.POST
    request_params_type = GetOrderDetailRequestBody
    response_type = GetOrderDetailResponse


class GetTradesApi(ExchangeRestApi):
    path = "private/margin/get-trades"
    method = HttpMethods.POST
    request_params_type = GetTradesRequestBody
    response_type = GetTradesResponse


class AdjustMarginLeverageApi(ExchangeRestApi):
    path = "private/margin/adjust-margin-leverage"
    method = HttpMethods.POST
    request_params_type = AdjustMarginLeverageRequestBody
    response_type = AdjustMarginLeverageResponse


class GetMarginTradingUserApi(ExchangeRestApi):
    path = "private/margin/get-margin-trading-user"
    method = HttpMethods.POST
    request_params_type = GetMarginTradingUserRequestBody
    response_type = GetMarginTradingUserResponse


class MarginService(ExchangeRestService):
    def get_transfer_history(
        self,
        direction: str,
        currency: str = None,
        start_ts: int = None,
        end_ts: int = None,
        page_size: int = None,
        page: int = None,
    ) -> GetTransferHistoryResponse:
        """request private/margin/get-transfer-history

        Args:
            direction (str): Transfer direction into or out of Margin Wallet E.g. IN or OUT
            currency (str, optional): Currency being transferred E.g. BTC, CRO or omit for 'all'. Defaults to None.
            start_ts (int, optional): Default is 24 hours ago from current timestamp. Defaults to None.
            end_ts (int, optional): Default is current timestamp. Defaults to None.
            page_size (int, optional): Page size (Default: 20, Max: 200). Defaults to None.
            page (int, optional): Page number (0-based). Defaults to None.

        Returns:
            GetTransferHistoryResponse: GetTransferHistoryResponse
        """
        api = GetTransferHistoryApi(host=self.host, _session=self.session)
        payload = GetTransferHistoryRequestBody(
            params=GetTransferHistoryRequestParams(
                direction=direction, currency=currency, start_ts=start_ts, end_ts=end_ts, page_size=page_size, page=page
            ),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = GetTransferHistoryResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def transfer(
        self,
        currency: str,
        from_side: str,
        to: str,
        amount: Union[int, Decimal],
    ) -> TransferResponse:
        """request private/margin/transfer

        Args:
            currency (str): Transfer currency, e.g. BTC, CRO
            from_side (str): SPOT or MARGIN
            to (str): SPOT or MARGIN
            amount (Union[int, Decimal]): The amount to be transferred

        Returns:
            TransferResponse: TransferResponse
        """
        api = TransferApi(host=self.host, _session=self.session)
        params = {
            "currency": currency,
            "from": from_side,
            "to": to,
            "amount": amount,
        }
        payload = TransferRequestBody(
            params=TransferRequestParams(**params),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True, by_alias=True)
        response = TransferResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def get_user_config(self) -> GetUserConfigResponse:
        """
        request private/margin/get-user-config
        Returns:
            GetUserConfigResponse
        """
        api = GetUserConfigApi(host=self.host, _session=self.session)
        payload = GetUserConfigRequestBody(params={}, api_key=self.api_key, secret_key=self.secret_key).json(
            exclude_none=True
        )
        response = GetUserConfigResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def get_account_summary(self) -> GetAccountSummaryResponse:
        """
        request private/margin/get-account-summary
        Returns:
            GetAccountSummaryResponse
        """
        api = GetAccountSummaryApi(host=self.host, _session=self.session)
        payload = GetAccountSummaryRequestBody(params={}, api_key=self.api_key, secret_key=self.secret_key).json(
            exclude_none=True
        )
        response = GetAccountSummaryResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def borrow(self, currency: str, amount: Decimal) -> BorrowResponse:
        """request private/margin/borrow
        Args:
            currency: Borrow currency, e.g. BTC, CRO
            amount: The amount to be borrowed
        Returns:
            BorrowResponse
        """
        api = BorrowApi(host=self.host, _session=self.session)
        payload = BorrowRequestBody(
            params=BorrowRequestParams(currency=currency, amount=amount),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = BorrowResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def repay(self, currency: str, amount: Decimal) -> RepayResponse:
        """
        request private/margin/repay
        Args:
            currency: Repay currency, e.g. BTC, CRO
            amount: The amount to be rapaid

        Returns:
            RepayResponse
        """
        api = RepayApi(host=self.host, _session=self.session)
        payload = RepayRequestBody(
            params=RepayRequestParams(currency=currency, amount=amount),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = RepayResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def get_borrow_history(
        self, currency: str = None, start_ts: int = None, end_ts: int = None, page_size: int = None, page: int = None
    ) -> GetBorrowHistoryResponse:
        """
        request private/margin/get-borrow-history
        Args:
            currency: Currency being borrowed E.g. BTC, CRO or omit for 'all'
            start_ts: Default is 24 hours ago from current timestamp
            end_ts: Default is current timestamp
            page_size: Page size (Default: 20, Max: 200)
            page: Page number (0-based)

        Returns:
            GetBorrowHistoryResponse
        """
        params = {"currency": currency, "start_ts": start_ts, "end_ts": end_ts, "page_size": page_size, "page": page}
        api = GetBorrowHistoryApi(host=self.host, _session=self.session)
        payload = GetBorrowHistoryRequestBody(
            params=GetBorrowHistoryRequestParams(**params), api_key=self.api_key, secret_key=self.secret_key
        ).json(exclude_none=True)
        response = GetBorrowHistoryResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def get_interest_history(
        self, currency: str = None, start_ts: int = None, end_ts: int = None, page_size: int = None, page: int = None
    ) -> GetInterestHistoryResponse:
        """
        request private/margin/get-interest-history
        Args:
            currency:
            start_ts: Default is 24 hours ago from the current timestamp. Max time range is 1 month
            end_ts: Default is current timestamp
            page_size: Page size (Default: 20, Max: 200)
            page: Page number (0-based)

        Returns:
            GetInterestHistoryResponse
        """
        params = {"currency": currency, "start_ts": start_ts, "end_ts": end_ts, "page": page, "page_size": page_size}
        api = GetInterestHistoryApi(host=self.host, _session=self.session)
        payload = GetInterestHistoryRequestBody(
            params=GetInterestHistoryRequestParams(**params), api_key=self.api_key, secret_key=self.secret_key
        ).json(exclude_none=True)
        response = GetInterestHistoryResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def get_repay_history(
        self, currency: str = None, start_ts: int = None, end_ts: int = None, page_size: int = None, page: int = None
    ) -> GetRepayHistoryResponse:
        """
        request private/margin/get-repay-history
        Args:
            currency: Currency of loan that was repaid E.g. BTC, CRO or omit for 'all'
            start_ts: Default is 24 hours ago from the current timestamp.
            end_ts: Default is current timestamp
            page_size: Page size (Default: 20, Max: 200)
            page: Page number (0-based)

        Returns:
            GetRepayHistoryResponse
        """
        params = {"currency": currency, "start_ts": start_ts, "end_ts": end_ts, "page": page, "page_size": page_size}
        api = GetRepayHistoryApi(host=self.host, _session=self.session)
        payload = GetRepayHistoryRequestBody(
            params=GetRepayHistoryRequestParams(**params), api_key=self.api_key, secret_key=self.secret_key
        ).json(exclude_none=True)
        response = GetRepayHistoryResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def get_liquidation_history(
        self,
        liquidation_status: str = None,
        start_ts: int = None,
        end_ts: int = None,
        page_size: int = None,
        page: int = None,
    ) -> GetLiquidationHistoryResponse:
        """
        request private/margin/get-liquidation-history
        Args:
            liquidation_status (str, optional):
            start_ts (int, optional):
            end_ts (int, optional):
            page_size (int, optional):
            page (int, optional):

        Returns:
            GetLiquidationHistoryResponse
        """
        params = {
            "liquidation_status": liquidation_status,
            "start_ts": start_ts,
            "end_ts": end_ts,
            "page": page,
            "page_size": page_size,
        }
        api = GetLiquidationHistoryApi(host=self.host, _session=self.session)
        payload = GetLiquidationHistoryRequestBody(
            params=GetLiquidationHistoryRequestParams(**params), api_key=self.api_key, secret_key=self.secret_key
        ).json(exclude_none=True)
        response = GetLiquidationHistoryResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def get_liquidation_orders(
        self, start_ts: int = None, end_ts: int = None, page_size: int = None, page: int = None
    ) -> GetLiquidationOrdersResponse:
        """
        request private/margin/get-liquidation-orders
        Args:
            start_ts: Default is 24 hours ago from the current timestamp.
            end_ts: Default is current timestamp， Max date range between start_ts and end_ts: 30 days
            page_size: Page size (Default: 20, Max: 200)
            page: Page number (0-based)

        Returns:
            GetLiquidationOrdersResponse
        """
        params = {
            "start_ts": start_ts,
            "end_ts": end_ts,
            "page": page,
            "page_size": page_size,
        }
        api = GetLiquidationOrdersApi(host=self.host, _session=self.session)
        payload = GetLiquidationOrdersRquestBody(
            params=GetLiquidationOrdersRequestParams(**params), api_key=self.api_key, secret_key=self.secret_key
        ).json(exclude_none=True)
        response = GetLiquidationOrdersResponse.parse_raw(b=api.call(data=payload).content)
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

    def cancel_order(self, instrument_name: str, order_id: str) -> CancelOrderResponse:
        """
        request private/margin/cancel-order
        Args:
            instrument_name: instrument_name, e.g., ETH_CRO, BTC_USDT
            order_id: Order ID

        Returns:
            CancelOrderResponse
        """
        api = CancelOrderApi(host=self.host, _session=self.session)
        params = {"instrument_name": instrument_name, "order_id": order_id}
        payload = CancelOrderRequestBody(
            params=CancelOrderRequestParams(**params), api_key=self.api_key, secret_key=self.secret_key
        ).json(exclude_none=True)
        response = CancelOrderResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def cancel_all_orders(self, instrument_name: str) -> CancelAllOrdersResponse:
        """
        request private/margin/cancel-all-orders
        Args:
            instrument_name: e.g. ETH_CRO, BTC_USDT

        Returns:
            CancelAllOrdersResponse
        """
        api = CancelAllOrdersApi(host=self.host, _session=self.session)
        params = {"instrument_name": instrument_name}
        payload = CancelAllOrdersRequestBody(
            params=CancelAllOrdersRequestParams(**params), api_key=self.api_key, secret_key=self.secret_key
        ).json(exclude_none=True)
        response = CancelAllOrdersResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def get_order_history(
        self,
        instrument_name: str = None,
        start_ts: int = None,
        end_ts: int = None,
        page_size: int = None,
        page: int = None,
    ) -> GetOrderHistoryResponse:
        """
        request private/margin/get-order-history
        Args:
            instrument_name: e.g. ETH_CRO, BTC_USDT. Omit for 'all'
            strart_ts: Start timestamp (milliseconds since the Unix epoch) - defaults to 24 hours ago
            end_ts: End timestamp (milliseconds since the Unix epoch) - defaults to 'now'
            page_size: Page size (Default: 20, max: 200)
            page: Page number (0-based)

        Returns:
            GetOrderHistoryResponse
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

    def get_open_orders(
        self, instrument_name: str = None, page_size: int = None, page: int = None
    ) -> GetOpenOrderResponse:
        """
        rrequest privte/margin/get-open-orders
        Args:
            instrument_name: instrument_name, e.g., ETH_CRO, BTC_USDT. Omit for "all"
            page_size: Page size (Default: 20, max: 200)
            page: Page number (0-based)

        Returns:
            GetOpenOrderResponse
        """
        params = {"instrument_name": instrument_name, "page_size": page_size, "page": page}
        api = GetOpenOrdersApi(host=self.host, _session=self.session)
        payload = GetOpenOrderRequestBody(
            params=GetOpenOrdersRequestParams(**params), api_key=self.api_key, secret_key=self.secret_key
        ).json(exclude_none=True)
        response = GetOpenOrderResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def get_order_detail(self, order_id: str) -> GetOrderDetailResponse:
        """
        request private/margin/get-order-detail
        Args:
            order_id: Order ID

        Returns:
            GetOrderDetailResponse
        """
        params = {"order_id": order_id}
        api = GetOrderDetailApi(host=self.host, _session=self.session)
        payload = GetOrderDetailRequestBody(
            params=GetOrderDetailRequestParams(**params), api_key=self.api_key, secret_key=self.secret_key
        ).json(exclude_none=True)
        response = GetOrderDetailResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def get_trades(
        self,
        instrument_name: str = None,
        start_ts: int = None,
        end_ts: int = None,
        page_size: int = None,
        page: int = None,
    ) -> GetTradesResponse:
        """
        request private/margin/get-trades
        Args:
            instrument_name: e.g. ETH_CRO, BTC_USDT. Omit for 'all'
            start_ts: Start timestamp (milliseconds since the Unix epoch) - defaults to 24 hours ago
            end_ts: End timestamp (milliseconds since the Unix epoch) - defaults to 'now'
            page_size: Page size (Default: 20, max: 200)
            page: Page number (0-based)

        Returns:
            GetTradesResponse
        """
        params = {
            "instrument_name": instrument_name,
            "start_ts": start_ts,
            "end_ts": end_ts,
            "page_size": page_size,
            "page": page,
        }
        api = GetTradesApi(host=self.host, _session=self.session)
        payload = GetTradesRequestBody(
            params=GetTradesRequestParams(**params), api_key=self.api_key, secret_key=self.secret_key
        ).json(exclude_none=True)
        response = GetTradesResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def adjust_margin_leverage(self, target_leverage: int):
        """
        Adjust Margin Leverage to target_leverage
        :param target_leverage: it can be 3, 5, 10
        :return:
            AdjustMarginLeverageResponse
        """
        params = {"target_leverage": target_leverage}
        api = AdjustMarginLeverageApi(host=self.host, _session=self.session)
        payload = AdjustMarginLeverageRequestBody(
            params=AdjustMarginLeverageRequestParams(**params), api_key=self.api_key, secret_key=self.secret_key
        ).json(exclude_none=True)
        response = AdjustMarginLeverageResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def get_margin_trading_user(self):
        """
        Get margin trading user - target leverage
        :return:
            GetMarginTradingUserResponse
        """
        api = GetMarginTradingUserApi(host=self.host, _session=self.session)
        payload = GetMarginTradingUserRequestBody(params={}, api_key=self.api_key, secret_key=self.secret_key).json(
            exclude_none=True
        )
        response = GetMarginTradingUserResponse.parse_raw(b=api.call(data=payload).content)
        return response
