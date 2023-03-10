from cdc.qa.apis.common.models.rest_api import HttpMethods

from ..fe_sp_base import SalesPortalApi, SalesPortalRestService
from ..models.sales_portal import (
    ConfirmQuoteRequestBody,
    ConfirmQuoteRequestParams,
    ConfirmQuoteResponse,
    GetExchangePriceRequestBody,
    GetExchangePriceRequestParams,
    GetExchangePriceResponse,
    GetInstrumentsRequestBody,
    GetInstrumentsResponse,
    GetOtcUserBalanceRequestBody,
    GetOtcUserBalanceResponse,
    GetOTCUserRequestBody,
    GetOTCUserRequestParams,
    GetOTCUserResponse,
    GetQuoteHistoryRequestBody,
    GetQuoteHistoryRequestParams,
    GetQuoteHistoryResponse,
    GetQuoteRequestBody,
    GetQuoteRequestParams,
    GetQuoteResponse,
    GetTradeHistoryRequestBody,
    GetTradeHistoryRequestParams,
    GetTradeHistoryResponse,
)


class GetOTCUserApi(SalesPortalApi):
    """Get OTC User."""

    path = "fe-sp-api/get-otc-user"
    method = HttpMethods.POST
    request_data_type = GetOTCUserRequestBody
    response_type = GetOTCUserResponse


class GetInstrumentsApi(SalesPortalApi):
    """Get tradable OTC instruments."""

    path = "fe-sp-api/get-instruments"
    method = HttpMethods.POST
    request_data_type = GetInstrumentsRequestBody
    response_type = GetInstrumentsResponse


class GetQuoteApi(SalesPortalApi):
    """Request a quote to buy or sell with either base currency or quote currency."""

    path = "fe-sp-api/get-quote"
    method = HttpMethods.POST
    request_data_type = GetQuoteRequestBody
    response_type = GetQuoteResponse


class ConfirmQuoteApi(SalesPortalApi):
    """Accept a quote from request quote."""

    path = "fe-sp-api/confirm-quote"
    method = HttpMethods.POST
    request_data_type = ConfirmQuoteRequestBody
    response_type = ConfirmQuoteResponse


class GetQuoteHistoryApi(SalesPortalApi):
    """Get quote history."""

    path = "fe-sp-api/get-quote-history"
    method = HttpMethods.POST
    request_data_type = GetQuoteHistoryRequestBody
    response_type = GetQuoteHistoryResponse


class GetTradeHistoryApi(SalesPortalApi):
    """Get trade history."""

    path = "fe-sp-api/get-trade-history"
    method = HttpMethods.POST
    request_data_type = GetTradeHistoryRequestBody
    response_type = GetTradeHistoryResponse


class GetOtcUserBalanceApi(SalesPortalApi):
    """Get otc user balance."""

    path = "fe-sp-api/get-otc-user-balance"
    method = HttpMethods.POST
    request_data_type = GetOtcUserBalanceRequestBody
    response_type = GetOtcUserBalanceResponse


class GetExchangePriceApi(SalesPortalApi):
    """Get exchange price."""

    path = "fe-sp-api/get-exchange-price"
    method = HttpMethods.POST
    request_data_type = GetExchangePriceRequestBody
    response_type = GetExchangePriceResponse


class SalesPortalService(SalesPortalRestService):
    def get_otc_user(self, account_email: str) -> GetOTCUserResponse:
        """request fe-sp-api/get-otc-user
        Returns:
            GetOTCUserResponse: GetOTCUserResponse
        """
        api = GetOTCUserApi(host=self.host, _session=self.session, token=self.token)
        payload = GetOTCUserRequestBody(
            params=GetOTCUserRequestParams(
                account_email=account_email,
            )
        ).json(exclude_none=True)
        response = GetOTCUserResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def get_instruments(self) -> GetInstrumentsResponse:
        """request fe-sp-api/get-instruments
        Returns:
            GetInstrumentsResponse: GetInstrumentsResponse
        """
        api = GetInstrumentsApi(host=self.host, _session=self.session, token=self.token)
        payload = GetInstrumentsRequestBody().json(exclude_none=True)
        response = GetInstrumentsResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def get_quote(
        self,
        on_behalf_account: str,
        base_currency: str,
        quote_currency: str,
        direction: str,
        base_currency_size: str = None,
        quote_currency_size: str = None,
    ) -> GetQuoteResponse:
        """request fe-sp-api/get-quote
        Args:
            on_behalf_account (str): Account uuid
            base_currency(string): Base currency, e.g. BTC, ETH
            quote_currency(string): Quote currency, e.g. USDT, USDC
            base_currency_size(string): Requested base currency size.
                                        Either use base_currency_size or quote_currency_size not both
            quote_currency_size(string): Requested quote currency size.
                                         Either use base_currency_size or quote_currency_size not both
            direction(string):  - BUY
                                - SELL
                                - TWO-WAY (returns price for both buy and sell)
        Returns:
            GetQuoteResponse: GetQuoteResponse
        """
        if base_currency_size is None and quote_currency_size is None:
            raise ValueError("at last one params of base_currency_size and quote_currency_size")
        if base_currency_size is not None and quote_currency_size is not None:
            raise ValueError("Either use base_currency_size or quote_currency_size not both")

        api = GetQuoteApi(host=self.host, _session=self.session, token=self.token, on_behalf_account=on_behalf_account)
        payload = GetQuoteRequestBody(
            params=GetQuoteRequestParams(
                base_currency=base_currency,
                quote_currency=quote_currency,
                direction=direction,
                base_currency_size=base_currency_size,
                quote_currency_size=quote_currency_size,
            )
        ).json(exclude_none=True)
        response = GetQuoteResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def confirm_quote(
        self,
        on_behalf_account: str,
        quote_id: str,
        quote: str,
        sales_margin: str,
        direction: str = None,
    ) -> ConfirmQuoteResponse:
        """request fe-sp-api/accept-quote
        Args:
            on_behalf_account (str): Account uuid
            quote_id (str): Quote Id from request quote
            quote (str): Quote from request quote
            sales_margin (str): Sales_margin from request quote
            direction (str, optional): BUY or SELL if requested quote using TWO-WAY. Defaults to None.
        Returns:
            ConfirmQuoteResponse: ConfirmQuoteResponse
        """
        api = ConfirmQuoteApi(
            host=self.host,
            _session=self.session,
            token=self.token,
            on_behalf_account=on_behalf_account,
        )
        payload = ConfirmQuoteRequestBody(
            params=ConfirmQuoteRequestParams(
                quote_id=quote_id,
                quote=quote,
                sales_margin=sales_margin,
                direction=direction,
            )
        ).json(exclude_none=True)
        response = ConfirmQuoteResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def get_quote_history(
        self,
        base_currency: str = None,
        quote_currency: str = None,
        start_ts: int = None,
        end_ts: int = None,
        page_size: int = None,
        page: int = None,
    ) -> GetQuoteHistoryResponse:
        """request fe-sp-api/get-quote-history
        Args:
            base_currency (str, optional): Base currency, e.g. BTC, ETH or omit for 'all'. Defaults to None.
            quote_currency (str, optional): Quote currency, e.g. USDT, USDC or omit for 'all'. Defaults to None.
            start_ts (int, optional): Default is 24 hours ago from current timestamp. Defaults to None.
            end_ts (int, optional): Default is current timestamp. Defaults to None.
            page_size (int, optional): Page size (Default: 20, Max: 200). Defaults to None.
            page (int, optional): Page number (0-based). Defaults to None.
        Returns:
            GetQuoteHistoryResponse: GetQuoteHistoryResponse
        """
        api = GetQuoteHistoryApi(host=self.host, _session=self.session, token=self.token)
        payload = GetQuoteHistoryRequestBody(
            params=GetQuoteHistoryRequestParams(
                base_currency=base_currency,
                quote_currency=quote_currency,
                start_ts=start_ts,
                end_ts=end_ts,
                page_size=page_size,
                page=page,
            )
        ).json(exclude_none=True)
        response = GetQuoteHistoryResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def get_trade_history(
        self,
        base_currency: str = None,
        quote_currency: str = None,
        start_ts: int = None,
        end_ts: int = None,
        page_size: int = None,
        page: int = None,
    ) -> GetTradeHistoryResponse:
        """request fe-sp-api/get-quote-history
        Args:
            base_currency (str, optional): Base currency, e.g. BTC, ETH or omit for 'all'. Defaults to None.
            quote_currency (str, optional): Quote currency, e.g. USDT, USDC or omit for 'all'. Defaults to None.
            start_ts (int, optional): Default is 24 hours ago from current timestamp. Defaults to None.
            end_ts (int, optional): Default is current timestamp. Defaults to None.
            page_size (int, optional): Page size (Default: 20, Max: 200). Defaults to None.
            page (int, optional): Page number (0-based). Defaults to None.
        Returns:
            GetTradeHistoryResponse: GetTradeHistoryResponse
        """
        api = GetTradeHistoryApi(host=self.host, _session=self.session, token=self.token)
        payload = GetTradeHistoryRequestBody(
            params=GetTradeHistoryRequestParams(
                base_currency=base_currency,
                quote_currency=quote_currency,
                start_ts=start_ts,
                end_ts=end_ts,
                page_size=page_size,
                page=page,
            )
        ).json(exclude_none=True)
        response = GetTradeHistoryResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def get_otc_user_balance(self, on_behalf_account: str) -> GetOtcUserBalanceResponse:
        """request fe-sp-api/get-quote-history
        Args:
            on_behalf_account (str): Account uuid
        Returns:
            GetTradeHistoryResponse: GetTradeHistoryResponse
        """
        api = GetOtcUserBalanceApi(
            host=self.host,
            _session=self.session,
            token=self.token,
            on_behalf_account=on_behalf_account,
        )
        payload = GetOtcUserBalanceRequestBody().json(exclude_none=True)
        response = GetOtcUserBalanceResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def get_exchange_price(self, symbol: str) -> GetExchangePriceResponse:
        """request fe-sp-api/get-exchange-price
        Args:
            symbol (str): symbol. e.g: BTC_USDT
        Returns:
            GetExchangePriceResponse: GetExchangePriceResponse
        """
        api = GetExchangePriceApi(host=self.host, _session=self.session, token=self.token)
        payload = GetExchangePriceRequestBody(
            params=GetExchangePriceRequestParams(symbol=symbol),
        ).json(exclude_none=True)
        response = GetExchangePriceResponse.parse_raw(b=api.call(data=payload).content)
        return response
