from ..fe_base import FeExchangeApi, FeExchangeRestService
from ..models.sub_account import (
    SuspendSubAccountRequest,
    SuspendSubAccountParams,
    SuspendSubAccountResponse,
    UnSuspendSubAccountRequest,
    UnSuspendSubAccountResponse,
    UnSuspendSubAccountParams,
    TerminateSubAccountRequest,
    TerminateSubAccountResponse,
    TerminateSubAccountParams,
    AddSubAccountRequest,
    AddSubAccountResponse,
    AddSubAccountParams,
    UpdateSubAccountParams,
    UpdateSubAccountRequest,
    UpdateSubAccountResponse,
)
from cdc.qa.apis.common.models.rest_api import HttpMethods


class SuspendSubAccountApi(FeExchangeApi):
    path = "subaccount/suspend-sub-account"
    method = HttpMethods.POST
    request_params_type = SuspendSubAccountRequest
    response_type = SuspendSubAccountResponse


class UnSuspendSubAccountApi(FeExchangeApi):
    path = "subaccount/unsuspend-sub-account"
    method = HttpMethods.POST
    request_params_type = UnSuspendSubAccountRequest
    response_type = UnSuspendSubAccountResponse


class TerminateSubAccountApi(FeExchangeApi):
    path = "subaccount/terminate-sub-account"
    method = HttpMethods.POST
    request_params_type = TerminateSubAccountRequest
    response_type = TerminateSubAccountResponse


class AddSubAccountApi(FeExchangeApi):
    path = "subaccount/add-sub-account"
    method = HttpMethods.POST
    request_params_type = AddSubAccountRequest
    response_type = AddSubAccountResponse


class UpdateSubAccountApi(FeExchangeApi):
    path = "subaccount/update-sub-account"
    method = HttpMethods.POST
    request_params_type = UpdateSubAccountRequest
    response_type = UpdateSubAccountResponse


class SubAccountService(FeExchangeRestService):
    def suspend_sub_account(self, uuid: str) -> SuspendSubAccountResponse:
        """request suspend-sub-account
        Args:
            uuid (int): User uuid of the sub account.
        Returns:
            response: SuspendSubAccountResponse
        """
        api = SuspendSubAccountApi(host=self.host, _session=self.session, exchange_token=self.exchange_token)
        payload = SuspendSubAccountRequest(params=SuspendSubAccountParams(uuid=uuid)).json(exclude_none=True)
        response = SuspendSubAccountResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def unsuspend_sub_account(self, uuid: str) -> UnSuspendSubAccountResponse:
        """request unsuspend-sub-account
        Args:
            uuid (int): User uuid of the sub account.
        Returns:
            response: UnSuspendSubAccountResponse
        """
        api = UnSuspendSubAccountApi(host=self.host, _session=self.session, exchange_token=self.exchange_token)
        payload = UnSuspendSubAccountRequest(params=UnSuspendSubAccountParams(uuid=uuid)).json(exclude_none=True)
        response = UnSuspendSubAccountResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def terminate_sub_account(self, uuid: str) -> TerminateSubAccountResponse:
        """request terminate-sub-account
        Args:
            uuid (int): User uuid of the sub account.
        Returns:
            response: TerminateSubAccountResponse
        """
        api = TerminateSubAccountApi(host=self.host, _session=self.session, exchange_token=self.exchange_token)
        payload = TerminateSubAccountRequest(params=TerminateSubAccountParams(uuid=uuid)).json(exclude_none=True)
        response = TerminateSubAccountResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def add_sub_account(
        self,
        label: str,
        enabled: bool,
        tradable: bool,
        margin_access: str,
        derivatives_access: str,
        name: str = None,
        email: str = None,
        mobile_number: str = None,
        address: str = None,
    ) -> AddSubAccountResponse:
        """request add-sub-account
        Args:
            label (str): Label of the sub account
            enabled (bool): true or false
            tradable (bool): true or false
            margin_access (str): DEFAULT or DISABLED
            derivatives_access (str): DEFAULT or DISABLED
            name (str, optional): Name of the sub account
            email (str, optional): Email of the sub account
            mobile_number (str, optional): Mobile number of the sub account
            address (str, optional): Address of the sub account

        Returns:
            response: AddSubAccountResponse
        """
        api = AddSubAccountApi(host=self.host, _session=self.session, exchange_token=self.exchange_token)
        payload = AddSubAccountRequest(
            params=AddSubAccountParams(
                label=label,
                enabled=enabled,
                tradable=tradable,
                margin_access=margin_access,
                derivatives_access=derivatives_access,
                name=name,
                email=email,
                mobile_number=mobile_number,
                address=address,
            )
        ).json(exclude_none=True)
        response = AddSubAccountResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def update_sub_account(
        self,
        uuid: str,
        label: str,
        enabled: bool,
        tradable: bool,
        margin_access: str,
        derivatives_access: str,
    ) -> UpdateSubAccountResponse:
        """request update-sub-account
        Args:
            label (str): Label of the sub account
            enabled (bool): true or false
            tradable (bool): true or false
            margin_access (str): DEFAULT or DISABLED
            derivatives_access (str): DEFAULT or DISABLED

        Returns:
            response: UpdateSubAccountResponse
        """
        api = UpdateSubAccountApi(host=self.host, _session=self.session, exchange_token=self.exchange_token)
        payload = UpdateSubAccountRequest(
            params=UpdateSubAccountParams(
                uuid=uuid,
                label=label,
                enabled=enabled,
                tradable=tradable,
                margin_access=margin_access,
                derivatives_access=derivatives_access,
            )
        ).json(exclude_none=True)
        response = UpdateSubAccountResponse.parse_raw(b=api.call(data=payload).content)
        return response
