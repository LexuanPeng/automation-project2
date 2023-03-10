from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.exchange_derivatives.rest.rest_base import DerivativesRestApi, DerivativesRestService

from ..models.trades import (
    ConvertCollateralRequestBody,
    ConvertCollateralRequestParams,
    ConvertCollateralResponse,
    GetTradesRequestBody,
    GetTradesRequestParams,
    GetTradesResponse,
    GetTransactionsRequestBody,
    GetTransactionsRequestParams,
    GetTransactionsResponse,
)


class GetTradesApi(DerivativesRestApi):
    """exchange-private deriv get trades"""

    path = "private/get-trades"
    method = HttpMethods.POST
    request_data_type = GetTradesRequestBody
    response_type = GetTradesResponse


class GetTransactionsApi(DerivativesRestApi):
    """exchange-private deriv get transactions"""

    path = "private/get-transactions"
    method = HttpMethods.POST
    request_data_type = GetTransactionsRequestBody
    response_type = GetTransactionsResponse


class ConvertCollateralApi(DerivativesRestApi):
    """exchange-private deriv convert-collateral"""

    path = "private/convert-collateral"
    method = HttpMethods.POST
    request_data_type = ConvertCollateralRequestBody
    response_type = ConvertCollateralResponse


class TradesService(DerivativesRestService):
    def get_trades(
        self,
        instrument_name: str = None,
        start_time: int = None,
        end_time: int = None,
        limit: int = None,
    ) -> GetTradesResponse:
        """request get trades
        Args:
            instrument_name (str, optional): instrument name, None for allow. Defaults to None.
            start_time (int, optional): Start timestamp.
            end_time (int, optional): Start timestamp.
            limit (int, optional): Page size.

        Returns:
            response: GetTradesResponse
        """
        api = GetTradesApi(host=self.host, _session=self.session)
        payload = GetTradesRequestBody(
            params=GetTradesRequestParams(
                instrument_name=instrument_name, start_time=start_time, end_time=end_time, limit=limit
            ),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = GetTradesResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def get_transactions(
        self,
        instrument_name: str = None,
        journal_type: str = None,
        start_time: int = None,
        end_time: int = None,
        limit: int = None,
    ) -> GetTransactionsResponse:
        """request get transactions

        Args:
            instrument_name (str, optional): instrument name, None for allow. Defaults to None.
            journal_type (str, optional): Journal type would be TRADING, TRADE_FEE, WITHDRAW_FEE,
                WITHDRAW, DEPOSIT, ROLLBACK_DEPOSIT, ROLLBACK_WITHDRAW, FUNDING, REALIZED_PNL,
                INSURANCE_FUND, SOCIALIZED_LOSS, LIQUIDATION_FEE, SESSION_RESET, ADJUSTMENT,
                SESSION_SETTLE, UNCOVERED_LOSS, ADMIN_ADJUSTMENT, DELIST, SETTLEMENT_FEE,
                AUTO_CONVERSION, MANUAL_CONVERSION. Defaults to None.
            start_time (int, optional): Start time in Unix time format (inclusive). Defaults to None.
            end_time (int, optional): End time in Unix time format (exclusive). Defaults to None.
            limit (int, optional): The maximum number of trades to be retrievd before the end_time. Defaults to None.

        Returns:
            GetTransactionsResponse: GetTransactionsResponse
        """
        api = GetTransactionsApi(host=self.host, _session=self.session)
        payload = GetTransactionsRequestBody(
            params=GetTransactionsRequestParams(
                instrument_name=instrument_name,
                journal_type=journal_type,
                start_time=start_time,
                end_time=end_time,
                limit=limit,
            ),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = GetTransactionsResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def convert_collateral(
        self,
        from_instrument_name: str,
        to_instrument_name: str,
        from_quantity: str,
        client_oid: str = None,
        slippage_tolerance: str = None,
        floor_price: str = None,
    ) -> ConvertCollateralResponse:
        """request convert collateral

        Args:
            from_instrument_name (str): from instrument name
            to_instrument_name (str): to instrument name
            from_quantity (str): from quantity
            client_oid (str, optional): client oid. Defaults to None.
            slippage_tolerance (str, optional): e.g: 0.001000. Defaults to None.
            floor_price (str, optional): e.g:0.999999. Defaults to None.

        Returns:
            ConvertCollateralResponse: convert collateral response
        """
        api = ConvertCollateralApi(host=self.host, _session=self.session)
        payload = ConvertCollateralRequestBody(
            params=ConvertCollateralRequestParams(
                from_instrument_name=from_instrument_name,
                to_instrument_name=to_instrument_name,
                from_quantity=from_quantity,
                client_oid=client_oid,
                slippage_tolerance=slippage_tolerance,
                floor_price=floor_price,
            ),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = ConvertCollateralResponse.parse_raw(b=api.call(data=payload).content)

        return response
