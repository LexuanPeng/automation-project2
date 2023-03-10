from decimal import Decimal
from typing import Union

from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.exchange.rest.rest_base import ExchangeRestApi, ExchangeRestService

from ..models.deriv import (
    DerivGetTransferHistoryRequestBody,
    DerivGetTransferHistoryRequestParams,
    DerivGetTransferHistoryResponse,
    DerivTransferRequestBody,
    DerivTransferRequestParams,
    DerivTransferResponse,
)


class DerivTransferApi(ExchangeRestApi):
    """Transfers funds between derivative and spot wallet."""

    path = "private/deriv/transfer"
    method = HttpMethods.POST
    request_data_type = DerivTransferRequestBody
    response_type = DerivTransferResponse


class DerivGetTransferHistoryApi(ExchangeRestApi):
    """Get the transfer history between the Spot and Derivatives Wallet."""

    path = "private/deriv/get-transfer-history"
    method = HttpMethods.POST
    request_data_type = DerivGetTransferHistoryRequestBody
    response_type = DerivGetTransferHistoryResponse


class DerivService(ExchangeRestService):
    def get_transfer_history(
        self,
        direction: str,
        currency: str = None,
        start_ts: int = None,
        end_ts: int = None,
        page_size: int = None,
        page: int = None,
    ) -> DerivGetTransferHistoryResponse:
        """request private/deriv/get-transfer-history

        Args:
            direction (str): Transfer direction into or out of Derivatives Wallet E.g. IN or OUT
            currency (str, optional): Currency being transferred E.g. BTC, CRO or omit for 'all'. Defaults to None.
            start_ts (int, optional): Default is 24 hours ago from current timestamp. Defaults to None.
            end_ts (int, optional): Default is current timestamp. Defaults to None.
            page_size (int, optional): Page size (Default: 20, Max: 200). Defaults to None.
            page (int, optional): Page number (0-based). Defaults to None.

        Returns:
            DerivGetTransferHistoryResponse: DerivGetTransferHistoryResponse
        """
        api = DerivGetTransferHistoryApi(host=self.host, _session=self.session)
        payload = DerivGetTransferHistoryRequestBody(
            params=DerivGetTransferHistoryRequestParams(
                direction=direction, currency=currency, start_ts=start_ts, end_ts=end_ts, page_size=page_size, page=page
            ),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = DerivGetTransferHistoryResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def transfer(
        self,
        currency: str,
        from_side: str,
        to: str,
        amount: Union[int, Decimal],
    ) -> DerivTransferResponse:
        """request private/deriv/transfer

        Args:
            currency (str): Transfer currency, e.g. BTC, CRO
            from_side (str): SPOT or DERIVATIVES
            to (str): SPOT or DERIVATIVES
            amount (Union[int, Decimal]): The amount to be transferred

        Returns:
            DerivTransferResponse: DerivTransferResponse
        """
        api = DerivTransferApi(host=self.host, _session=self.session)
        params = {
            "currency": currency,
            "from": from_side,
            "to": to,
            "amount": amount,
        }
        payload = DerivTransferRequestBody(
            params=DerivTransferRequestParams(**params),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True, by_alias=True)
        response = DerivTransferResponse.parse_raw(b=api.call(data=payload).content)

        return response
