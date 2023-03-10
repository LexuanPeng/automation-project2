import logging
from typing import Optional, Union

from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.rails.models.withdraw import (
    WithdrawalWhitelistAddPayStringRequest,
    WithdrawalWhitelistAddPayStringResponse,
    WithdrawalAddressCreateRequestData,
    WithdrawalAddressCreateResponse,
    WithdrawalAddressesPathParams,
    WithdrawalAddressesResponse,
    WithdrawalLimitQueryParams,
    WithdrawalLimitResponse,
    WithdrawalFeeQueryParams,
    WithdrawalFeeResponse,
    WithdrawalCreateRequestData,
    WithdrawalCreateResponse,
)
from ..models import RailsRestApi, RailsRestService


logger = logging.getLogger(__name__)


class WithdrawalWhitelistAddPayStringApi(RailsRestApi):
    """Add paystring in withdrawal whitelist"""

    path = "withdrawal_pay_ids/create"
    method = HttpMethods.POST


class WithdrawalAddressCreateApi(RailsRestApi):
    """Create withdrawal address"""

    path = "withdrawal_addresses/create"
    method = HttpMethods.POST
    request_data_type = WithdrawalAddressCreateRequestData
    response_type = WithdrawalAddressCreateResponse


class WithdrawalAddressesApi(RailsRestApi):
    """Get withdrawal address by currency"""

    def path(self, path_params: WithdrawalAddressesPathParams):
        return f"withdrawal_addresses/currency/{path_params.currency}"

    method = HttpMethods.GET
    response_type = WithdrawalAddressesResponse


class WithdrawalLimitApi(RailsRestApi):
    """Get withdrawal limit by currency and network id"""

    path = "withdrawals/limit"
    method = HttpMethods.GET
    request_params_type = WithdrawalLimitQueryParams
    response_type = WithdrawalLimitResponse


class WithdrawalFeeApi(RailsRestApi):
    """Get withdrawal fee by amount, currency and network id"""

    path = "withdrawals/fee"
    method = HttpMethods.GET
    request_params_type = WithdrawalFeeQueryParams
    response_type = WithdrawalFeeResponse


class WithdrawalCreateApi(RailsRestApi):
    """Create withdrawal"""

    path = "withdrawals/create"
    method = HttpMethods.POST
    request_data_type = WithdrawalCreateRequestData
    response_type = WithdrawalCreateResponse


class WithdrawService(RailsRestService):
    def whitelist_add_paystring(
        self,
        otp: str,
        paystring_address: str,
        passcode: str,
    ) -> WithdrawalWhitelistAddPayStringResponse:
        api = WithdrawalWhitelistAddPayStringApi(host=self.host, _session=self.session)
        data = WithdrawalWhitelistAddPayStringRequest(
            otp=otp,
            pay_id=paystring_address,
            passcode=passcode,
        ).dict(exclude_none=True)
        response = api.call(data=data)
        return WithdrawalWhitelistAddPayStringResponse.parse_raw(b=response.content)

    def create_withdrawal_address(
        self,
        currency: str,
        network_id: str,
        address: str,
        label: str,
        passcode: str,
        otp: Optional[str],
    ) -> WithdrawalAddressCreateResponse:
        api = WithdrawalAddressCreateApi(host=self.host, _session=self.session)
        data = WithdrawalAddressCreateRequestData(
            currency=currency,
            address=address,
            label=label,
            network_id=network_id,
            passcode=passcode,
            otp=otp,
        ).dict(exclude_none=True)

        response = api.call(data=data)
        return WithdrawalAddressCreateResponse.parse_raw(b=response.content)

    def get_withdrawal_addresses_by_currency(self, currency: str) -> WithdrawalAddressesResponse:
        api = WithdrawalAddressesApi(host=self.host, _session=self.session)
        path_params = WithdrawalAddressesPathParams(currency=currency)

        response = api.call(path_params=path_params)
        return WithdrawalAddressesResponse.parse_raw(b=response.content)

    def get_withdrawal_limit(self, currency: str, network_id: str) -> WithdrawalLimitResponse:
        api = WithdrawalLimitApi(host=self.host, _session=self.session)
        params = WithdrawalLimitQueryParams(currency=currency, network_id=network_id).dict(exclude_none=True)

        response = api.call(params=params)
        return WithdrawalLimitResponse.parse_raw(b=response.content)

    def get_withdrawal_fee(self, currency: str, network_id: str, amount: str) -> WithdrawalFeeResponse:
        api = WithdrawalFeeApi(host=self.host, _session=self.session)
        params = WithdrawalFeeQueryParams(currency=currency, network_id=network_id, amount=amount).dict(
            exclude_none=True
        )

        response = api.call(params=params)
        return WithdrawalFeeResponse.parse_raw(b=response.content)

    def create_withdrawal(
        self,
        currency: str,
        address: str,
        amount: str,
        network_id: str,
        passcode: str,
        otp: Optional[str],
        phone_otp: Optional[str],
    ) -> WithdrawalCreateResponse:
        api = WithdrawalCreateApi(host=self.host, _session=self.session)
        data = WithdrawalCreateRequestData(
            currency=currency,
            address=address,
            amount=amount,
            network_id=network_id,
            passcode=passcode,
            otp=otp,
            phone_otp=phone_otp,
        ).dict(exclude_none=True)

        response = api.call(data=data)
        return WithdrawalCreateResponse.parse_raw(b=response.content)

    def create_withdrawal_with_travel_rule(
        self,
        currency: str,
        address: str,
        amount: Union[int, str],
        network_id: str,
        passcode: str,
        travel_rule_recipient_name: str,
        note: Optional[str],
        otp: Optional[str] = None,
        to_wallet_app: Optional[str] = "",
        phone_otp: Optional[str] = None,
    ) -> WithdrawalCreateResponse:
        api = WithdrawalCreateApi(host=self.host, _session=self.session)
        data = WithdrawalCreateRequestData(
            currency=currency,
            address=address,
            amount=amount,
            network_id=network_id,
            passcode=passcode,
            otp=otp,
            travel_rule_recipient_name=travel_rule_recipient_name,
            travel_rule_wallet_type=WithdrawalCreateRequestData.TravelRuleWalletType(id=3, name="Crypto.com").dict(
                exclude_none=True
            ),
            biometric=False,
            note=note,
            to_wallet_app="",
        ).dict(exclude_none=True)

        response = api.call(json=data)
        return WithdrawalCreateResponse.parse_raw(b=response.content)
