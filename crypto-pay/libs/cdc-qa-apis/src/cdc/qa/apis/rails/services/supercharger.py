import logging

from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.rails.models.supercharger import (
    SuperchargerAccountResponse,
    SuperchargerEventsQueryParams,
    SuperchargerEventsResponse,
    SuperchargerDepositTermsRequestData,
    SuperchargerDepositTermsResponse,
    SuperchargerDepositOrdersCreateRequestData,
    SuperchargerDepositOrdersCreateResponse,
    SuperchargerDepositsCreateRequestData,
    SuperchargerDepositsCreateResponse,
    SuperchargerWithdrawalOrdersCreateRequestData,
    SuperchargerWithdrawalOrdersCreateResponse,
    SuperchargerWithdrawalsCreateRequestData,
    SuperchargerWithdrawalsCreateResponse,
)
from ..models import RailsRestApi, RailsRestService


logger = logging.getLogger(__name__)


class SuperchargerAccountApi(RailsRestApi):
    """Get user supercharger account info"""

    path = "supercharger/account/show"
    method = HttpMethods.GET
    response_type = SuperchargerAccountResponse


class SuperchargerEventsApi(RailsRestApi):
    """Get supercharger events, filterd by is_completed"""

    path = "supercharger/events"
    method = HttpMethods.GET
    request_params_type = SuperchargerEventsQueryParams
    response_type = SuperchargerEventsResponse


class SuperchargerDepositTermsApi(RailsRestApi):
    """accept to supercharger deposit tnc"""

    path = "supercharger/deposits/tnc"
    method = HttpMethods.POST
    request_data_type = SuperchargerDepositTermsRequestData
    response_type = SuperchargerDepositTermsResponse


class SuperchargerDepositOrderApi(RailsRestApi):
    """Create supercharger deposit order"""

    path = "supercharger/deposits/orders/create"
    method = HttpMethods.POST
    request_data_type = SuperchargerDepositOrdersCreateRequestData
    response_type = SuperchargerDepositOrdersCreateResponse


class SuperchargerDepositCreateApi(RailsRestApi):
    """Create supercharger deposit"""

    path = "supercharger/deposits/create"
    method = HttpMethods.POST
    request_data_type = SuperchargerDepositsCreateRequestData
    response_type = SuperchargerDepositsCreateResponse


class SuperchargerWithdrawalOrderApi(RailsRestApi):
    """Create supercharger withdrawal order"""

    path = "supercharger/withdrawals/orders/create"
    method = HttpMethods.POST
    request_data_type = SuperchargerWithdrawalOrdersCreateRequestData
    response_type = SuperchargerWithdrawalOrdersCreateResponse


class SuperchargerWithdrawalCreateApi(RailsRestApi):
    """Create supercharger withdrawal"""

    path = "supercharger/withdrawals/create"
    method = HttpMethods.POST
    request_data_type = SuperchargerWithdrawalsCreateRequestData
    response_type = SuperchargerWithdrawalsCreateResponse


class SuperchargerService(RailsRestService):
    def get_account(self) -> SuperchargerAccountResponse:
        api = SuperchargerAccountApi(host=self.host, _session=self.session)
        response = api.call()
        return SuperchargerAccountResponse.parse_raw(b=response.content)

    def get_events(self, is_completed: int) -> SuperchargerEventsResponse:
        api = SuperchargerEventsApi(host=self.host, _session=self.session)
        params = SuperchargerEventsQueryParams(is_completed=is_completed).dict(exclude_none=True)
        response = api.call(params=params)
        return SuperchargerEventsResponse.parse_raw(b=response.content)

    def accept_deposit_tnc(self) -> SuperchargerDepositTermsResponse:
        api = SuperchargerDepositTermsApi(host=self.host, _session=self.session)
        data = SuperchargerDepositTermsRequestData(accepted=True).dict(exclude_none=True)
        response = api.call(data=data)
        return SuperchargerDepositTermsResponse.parse_raw(b=response.content)

    def create_deposit_order(
        self, event_id: str, currency: str, amount: str
    ) -> SuperchargerDepositOrdersCreateResponse:
        api = SuperchargerDepositOrderApi(host=self.host, _session=self.session)
        data = SuperchargerDepositOrdersCreateRequestData(
            event_id=event_id,
            currency=currency,
            amount=amount,
        ).dict(exclude_none=True)
        response = api.call(data=data)
        return SuperchargerDepositOrdersCreateResponse.parse_raw(b=response.content)

    def create_deposit(self, passcode: str, order_id: str) -> SuperchargerDepositsCreateResponse:
        api = SuperchargerDepositCreateApi(host=self.host, _session=self.session)
        data = SuperchargerDepositsCreateRequestData(passcode=passcode, supercharger_deposit_order_id=order_id).dict(
            exclude_none=True
        )
        response = api.call(data=data)
        return SuperchargerDepositsCreateResponse.parse_raw(b=response.content)

    def create_withdrawal_order(
        self, event_id: str, currency: str, amount: str
    ) -> SuperchargerWithdrawalOrdersCreateResponse:
        api = SuperchargerWithdrawalOrderApi(host=self.host, _session=self.session)
        data = SuperchargerWithdrawalOrdersCreateRequestData(
            event_id=event_id,
            currency=currency,
            amount=amount,
        ).dict(exclude_none=True)
        response = api.call(data=data)
        return SuperchargerWithdrawalOrdersCreateResponse.parse_raw(b=response.content)

    def create_withdrawal(self, passcode: str, order_id: str) -> SuperchargerWithdrawalsCreateResponse:
        api = SuperchargerWithdrawalCreateApi(host=self.host, _session=self.session)
        data = SuperchargerWithdrawalsCreateRequestData(
            passcode=passcode, supercharger_withdrawal_order_id=order_id
        ).dict(exclude_none=True)
        response = api.call(data=data)
        return SuperchargerWithdrawalsCreateResponse.parse_raw(b=response.content)
