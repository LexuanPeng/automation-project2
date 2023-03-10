from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.exchange.rest.rest_base import ExchangeRestApi, ExchangeRestService

from ..models.sub_account import (
    GetSubAccountParams,
    GetSubAccountsResponse,
    GetSubAccountRequestBody,
    GetTransferHistoryRequestParams,
    GetTransferHistoryResponse,
    GetTransferHistoryBody,
    TransferRequestParams,
    TransferRequestBody,
    TransferResponse,
)


class GetSubAccountApi(ExchangeRestApi):
    path = "private/subaccount/get-sub-accounts"
    method = HttpMethods.POST
    request_data_type = GetSubAccountRequestBody
    response_type = GetSubAccountsResponse


class GetTransferHistoryApi(ExchangeRestApi):
    path = "private/subaccount/get-transfer-history"
    method = HttpMethods.POST
    request_data_type = GetTransferHistoryBody
    response_type = GetTransferHistoryResponse


class TransferApi(ExchangeRestApi):
    path = "private/subaccount/transfer"
    method = HttpMethods.POST
    request_data_type = TransferRequestBody
    response_type = TransferResponse


class SubAccountService(ExchangeRestService):
    def get_sub_accounts(self, page_size: int = None) -> GetSubAccountsResponse:
        """
        request get sub accounts
        Returns:
            GetSubAccountsResponse
        """
        api = GetSubAccountApi(host=self.host, _session=self.session)
        payload = GetSubAccountRequestBody(
            params=GetSubAccountParams(page_size=page_size),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = GetSubAccountsResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def get_transfer_history(
        self,
        sub_account_uuid: str,
        direction: str,
        currency: str = None,
        start_ts: int = None,
        end_ts: int = None,
        page_size: int = None,
        page: int = None,
    ) -> GetTransferHistoryResponse:
        """
        Get Sub Account Transfer History
        Args:
           sub_account_uuid:
           direction: Transfer direction into or out of Account E.g. IN or OUT
           currency: Currency being transferred E.g. BTC, CRO or omit for 'all'
           start_ts:
           end_ts:
           page_size: Page size (Default: 20, Max: 200)
           page: Page number (0-based)

        Returns:
            GetTransferHistoryResponse
        """
        api = GetTransferHistoryApi(host=self.host, _session=self.session)
        payload = GetTransferHistoryBody(
            params=GetTransferHistoryRequestParams(
                sub_account_uuid=sub_account_uuid,
                direction=direction,
                currency=currency,
                start_ts=start_ts,
                end_ts=end_ts,
                page_size=page_size,
                page=page,
            ),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True, by_alias=True)
        response = GetTransferHistoryResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def transfer(
        self,
        currency: str,
        transfer_from: str,
        to: str,
        sub_account_uuid: str,
        amount: str,
        from_wallet: str = None,
        to_wallet: str = None,
    ) -> TransferResponse:
        """
        Transfer amount between subaccount and master account
        Args:
            currency:
            transfer_from:
            to:
            sub_account_uuid:
            amount:
            from_wallet:
            to_wallet:

        Returns:
            TransferResponse
        """
        api = TransferApi(host=self.host, _session=self.session)
        params = {
            "currency": currency,
            "from": transfer_from,
            "from_wallet": from_wallet,
            "to": to,
            "to_wallet": to_wallet,
            "sub_account_uuid": sub_account_uuid,
            "amount": amount,
        }
        payload = TransferRequestBody(
            params=TransferRequestParams(**params),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True, by_alias=True)
        response = TransferResponse.parse_raw(b=api.call(data=payload).content)
        return response
