from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.exchange_oex.models import ExchangeRequestParams
from cdc.qa.apis.exchange_oex.rest.rest_base import ExchangeRestApi, ExchangeRestService

from ..models.otc import (
    AcceptQuoteRequestBody,
    AcceptQuoteRequestParams,
    AcceptQuoteResponse,
    GetInstrumentsRequestBody,
    GetInstrumentsResponse,
    GetOTCUserRequestBody,
    GetOTCUserResponse,
    GetQuoteHistoryRequestBody,
    GetQuoteHistoryRequestParams,
    GetQuoteHistoryResponse,
    GetTradeHistoryRequestBody,
    GetTradeHistoryRequestParams,
    GetTradeHistoryResponse,
    RequestQuoteRequestBody,
    RequestQuoteRequestParams,
    RequestQuoteResponse,
)


class GetOTCUserApi(ExchangeRestApi):
    """Get OTC User."""

    path = "private/otc/get-otc-user"
    method = HttpMethods.POST
    request_data_type = GetOTCUserRequestBody
    response_type = GetOTCUserResponse


class GetInstrumentsApi(ExchangeRestApi):
    """Get tradable OTC instruments."""

    path = "private/otc/get-instruments"
    method = HttpMethods.POST
    request_data_type = GetInstrumentsRequestBody
    response_type = GetInstrumentsResponse


class RequestQuoteApi(ExchangeRestApi):
    """Request a quote to buy or sell with either base currency or quote currency."""

    path = "private/otc/request-quote"
    method = HttpMethods.POST
    request_data_type = RequestQuoteRequestBody
    response_type = RequestQuoteResponse


class AcceptQuoteApi(ExchangeRestApi):
    """Accept a quote from request quote."""

    path = "private/otc/accept-quote"
    method = HttpMethods.POST
    request_data_type = AcceptQuoteRequestBody
    response_type = AcceptQuoteResponse


class GetQuoteHistoryApi(ExchangeRestApi):
    """Get quote history."""

    path = "private/otc/get-quote-history"
    method = HttpMethods.POST
    request_data_type = GetQuoteHistoryRequestBody
    response_type = GetQuoteHistoryResponse


class GetTradeHistoryApi(ExchangeRestApi):
    """Get trade history."""

    path = "private/otc/get-trade-history"
    method = HttpMethods.POST
    request_data_type = GetTradeHistoryRequestBody
    response_type = GetTradeHistoryResponse


class OTCService(ExchangeRestService):
    def get_otc_user(self, system_label: str = None) -> GetOTCUserResponse:
        """request private/otc/get-otc-user

        Returns:
            GetOTCUserResponse: GetOTCUserResponse
        """
        api = GetOTCUserApi(host=self.host, _session=self.session)
        payload = GetOTCUserRequestBody(
            api_key=self.api_key,
            secret_key=self.secret_key,
            params=ExchangeRequestParams(system_label=system_label),
        ).json(exclude_none=True)
        response = GetOTCUserResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def get_instruments(self, system_label: str = None) -> GetInstrumentsResponse:
        """request private/otc/get-instruments
        Returns:
            GetInstrumentsResponse: GetInstrumentsResponse
        """
        api = GetInstrumentsApi(host=self.host, _session=self.session)
        payload = GetInstrumentsRequestBody(
            api_key=self.api_key,
            secret_key=self.secret_key,
            params=ExchangeRequestParams(system_label=system_label),
        ).json(exclude_none=True)
        response = GetInstrumentsResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def request_quote(
        self,
        base_currency: str,
        quote_currency: str,
        direction: str,
        base_currency_size: str = None,
        quote_currency_size: str = None,
        system_label: str = None,
    ) -> RequestQuoteResponse:
        """request private/otc/request-quote

        Args:
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
            RequestQuoteResponse: RequestQuoteResponse
        """
        if base_currency_size is None and quote_currency_size is None:
            raise ValueError("at last one params of base_currency_size and quote_currency_size")
        if base_currency_size is not None and quote_currency_size is not None:
            raise ValueError("Either use base_currency_size or quote_currency_size not both")

        api = RequestQuoteApi(host=self.host, _session=self.session)
        payload = RequestQuoteRequestBody(
            params=RequestQuoteRequestParams(
                base_currency=base_currency,
                quote_currency=quote_currency,
                direction=direction,
                base_currency_size=base_currency_size,
                quote_currency_size=quote_currency_size,
                system_label=system_label,
            ),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = RequestQuoteResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def accept_quote(self, quote_id: str, direction: str = None, system_label: str = None) -> AcceptQuoteResponse:
        """request private/otc/accept-quote

        Args:
            quote_id (str): Quote Id from request quote
            direction (str, optional): BUY or SELL if requested quote using TWO-WAY. Defaults to None.

        Returns:
            AcceptQuoteResponse: AcceptQuoteResponse
        """
        api = AcceptQuoteApi(host=self.host, _session=self.session)
        payload = AcceptQuoteRequestBody(
            params=AcceptQuoteRequestParams(quote_id=quote_id, direction=direction, system_label=system_label),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True, by_alias=True)
        response = AcceptQuoteResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def get_quote_history(
        self,
        base_currency: str = None,
        quote_currency: str = None,
        start_ts: int = None,
        end_ts: int = None,
        page_size: int = None,
        page: int = None,
        system_label: str = None,
    ) -> GetQuoteHistoryResponse:
        """request private/otc/get-quote-history

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
        api = GetQuoteHistoryApi(host=self.host, _session=self.session)
        payload = GetQuoteHistoryRequestBody(
            params=GetQuoteHistoryRequestParams(
                base_currency=base_currency,
                quote_currency=quote_currency,
                start_ts=start_ts,
                end_ts=end_ts,
                page_size=page_size,
                page=page,
                system_label=system_label,
            ),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True, by_alias=True)
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
        system_label: str = None,
    ) -> GetTradeHistoryResponse:
        """request private/otc/get-quote-history

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
        api = GetTradeHistoryApi(host=self.host, _session=self.session)
        payload = GetTradeHistoryRequestBody(
            params=GetTradeHistoryRequestParams(
                base_currency=base_currency,
                quote_currency=quote_currency,
                start_ts=start_ts,
                end_ts=end_ts,
                page_size=page_size,
                page=page,
                system_label=system_label,
            ),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True, by_alias=True)
        response = GetTradeHistoryResponse.parse_raw(b=api.call(data=payload).content)
        return response
