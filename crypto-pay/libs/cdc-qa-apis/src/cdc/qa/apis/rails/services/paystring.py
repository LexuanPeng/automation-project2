import logging
import json

from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.rails.models.paystring import (
    PayStringEligibleResponse,
    RegisterPayStringRequestData,
    PayStringResponse,
    UpdatePayStringRequest,
)

from ..models import RailsRestApi, RailsRestService


logger = logging.getLogger(__name__)


class PayStringEligibilityApi(RailsRestApi):
    """Get PayString Eligibility"""

    path = "pay_ids/eligibility"
    method = HttpMethods.GET
    response_type = PayStringEligibleResponse


class RegisterPayStringApi(RailsRestApi):
    """Register PayString"""

    path = "pay_ids/create"
    method = HttpMethods.POST
    request_data = RegisterPayStringRequestData
    response_type = PayStringResponse


class ShowPayStringApi(RailsRestApi):
    """Show PayString settings"""

    path = "pay_ids/show"
    method = HttpMethods.GET
    response_data = PayStringResponse


class UpdatePayStringLinkedCoinsApi(RailsRestApi):
    """Update PayString linked coins"""

    path = "pay_ids/currencies/update"
    method = HttpMethods.POST
    request_data = UpdatePayStringRequest
    response_type = PayStringResponse


class PayStringService(RailsRestService):
    def get_eligibility(self) -> PayStringEligibleResponse:
        api = PayStringEligibilityApi(host=self.host, _session=self.session)
        response = api.call()
        return PayStringEligibleResponse.parse_raw(b=response.content)

    def register_paystring(self, paystring: str) -> PayStringResponse:
        api = RegisterPayStringApi(host=self.host, _session=self.session)
        payload = RegisterPayStringRequestData(acct_part=paystring).dict(exclude_none=True)
        headers = {"content-type": "application/json; charset=utf-8"}
        response = api.call(data=json.dumps(payload), headers=headers)
        return PayStringResponse.parse_raw(b=response.content)

    def get_paystring_info(self) -> PayStringResponse:
        api = ShowPayStringApi(host=self.host, _session=self.session)
        response = api.call()
        logger.info(response.content)
        return PayStringResponse.parse_raw(b=response.content)

    def update_paystring_linked_coins(self, currencies: list) -> PayStringResponse:
        api = UpdatePayStringLinkedCoinsApi(host=self.host, _session=self.session)
        logger.info(f"get currencies: {currencies}")
        payload = UpdatePayStringRequest(currencies=currencies).dict(exclude_none=True)
        headers = {"content-type": "application/json; charset=utf-8"}
        response = api.call(data=json.dumps(payload), headers=headers)
        return PayStringResponse.parse_raw(b=response.content)
