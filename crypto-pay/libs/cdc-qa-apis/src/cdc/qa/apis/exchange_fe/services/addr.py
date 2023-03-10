from typing import List

from cdc.qa.apis.common.models.rest_api import HttpMethods

from ..fe_base import FeExchangeApi, FeExchangeRestService
from ..models.addr import (
    AddressListRequest,
    AddressListResponse,
    AddWithdrawAddrRequest,
    AddWithdrawAddrResponse,
    DeleteWithdrawAddrRequest,
    DeleteWithdrawAddrResponse,
)


# addr/address_list
class AddressListApi(FeExchangeApi):
    path = "addr/address_list"
    method = HttpMethods.POST
    request_params_type = AddressListRequest
    response_type = AddressListResponse


# addr/add_withdraw_addr
class AddWithdrawAddrListApi(FeExchangeApi):
    path = "addr/add_withdraw_addr"
    method = HttpMethods.POST
    request_params_type = AddWithdrawAddrRequest
    response_type = AddWithdrawAddrResponse


# addr/delete_withdraw_addr
class DeleteWithdrawAddrListApi(FeExchangeApi):
    path = "addr/delete_withdraw_addr"
    method = HttpMethods.POST
    request_params_type = DeleteWithdrawAddrRequest
    response_type = DeleteWithdrawAddrResponse


class AddressService(FeExchangeRestService):
    def address_list(self, coin_symbol: str = None) -> AddressListResponse:
        """address list pai

        Args:
            coin_symbol (str): coin symbol. default None

        Returns:
            AddressListResponse: Address list response
        """
        api = AddressListApi(host=self.host, _session=self.session, exchange_token=self.exchange_token)
        payload = AddressListRequest(coinSymbol=coin_symbol).json(exclude_none=True)
        response = AddressListResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def add_withdraw_addr(
        self,
        coin_symbol: str,
        network: str,
        address: str,
        label: str,
        sms_otp: str,
        google_code: str,
        memo: str = None,
        destinationTag: str = None,
        isOwnerOfAddress: bool = True,
        recipientName: str = "",
        addressTypeId: int = 2,
    ) -> AddWithdrawAddrResponse:
        """add withdraw address

        Args:
            coin_symbol (str): coin symbol
            network (str): network
            address (str): address str
            label (str): address label
            sms_otp (str): sms code
            google_code (str): 2fa code
            memo (str, optional): memo. Defaults to None.
            destinationTag (str, optional): destinationTag. Defaults to None.

        Returns:
            AddWithdrawAddrResponse: add withdraw address response
        """
        api = AddWithdrawAddrListApi(host=self.host, _session=self.session, exchange_token=self.exchange_token)
        payload = AddWithdrawAddrRequest(
            coinSymbol=coin_symbol,
            network=network,
            address=address,
            label=label,
            smsOtp=sms_otp,
            googleCode=google_code,
            memo=memo,
            destinationTag=destinationTag,
            isOwnerOfAddress=isOwnerOfAddress,
            recipientName=recipientName,
            addressTypeId=addressTypeId,
        ).json(exclude_none=True)
        response = AddWithdrawAddrResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def delete_withdraw_addr(self, ids: List, sms_otp: str, google_code: str) -> DeleteWithdrawAddrResponse:
        """delete withdraw address

        Args:
            ids (List): address ids
            sms_otp (str): sms code
            google_code (str): google code for 2fa

        Returns:
            DeleteWithdrawAddrResponse: delete response
        """
        api = DeleteWithdrawAddrListApi(host=self.host, _session=self.session, exchange_token=self.exchange_token)
        payload = DeleteWithdrawAddrRequest(ids=ids, smsOtp=sms_otp, googleCode=google_code).json(exclude_none=True)
        response = DeleteWithdrawAddrResponse.parse_raw(b=api.call(data=payload).content)
        return response
