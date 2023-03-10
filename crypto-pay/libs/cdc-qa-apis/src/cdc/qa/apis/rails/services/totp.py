from cdc.qa.apis.common.models.rest_api import HttpMethods

from typing import List
from ..models import RailsRestApi, RailsRestService
from ..models.totp import (
    TotpCreateRequestData,
    TotpCreateResponse,
    TotpVerifyRequestData,
    TotpVerifyResponse,
    TotpDisableRequestData,
    TotpDisableResponse,
    TotpShowResponse,
)


class TotpCreateApi(RailsRestApi):
    """Create TOTP."""

    path = "totp/create"
    method = HttpMethods.POST
    request_data_type = TotpCreateRequestData
    response_type = TotpCreateResponse


class TotpVerifyApi(RailsRestApi):
    """Verify TOTP."""

    path = "totp/verify"
    method = HttpMethods.POST
    request_data_type = TotpVerifyRequestData
    response_type = TotpVerifyResponse


class TotpDisableApi(RailsRestApi):
    """Disable TOTP."""

    path = "totp/disable"
    method = HttpMethods.POST
    request_data_type = TotpDisableRequestData
    response_type = TotpDisableResponse


class TotpShowApi(RailsRestApi):
    """Show TOTP Details"""

    path = "totp/show"
    method = HttpMethods.GET
    response_type = TotpShowResponse


class TotpService(RailsRestService):
    def create(self, passcode: str) -> TotpCreateResponse:
        api = TotpCreateApi(host=self.host, _session=self.session)
        data = TotpCreateRequestData(passcode=passcode).dict(exclude_none=True)

        response = api.call(data=data)
        return TotpCreateResponse.parse_raw(b=response.content)

    def verify(self, otp: str) -> TotpVerifyResponse:
        api = TotpVerifyApi(host=self.host, _session=self.session)
        data = TotpVerifyRequestData(otp=otp).dict(exclude_none=True)

        response = api.call(data=data)
        return TotpVerifyResponse.parse_raw(b=response.content)

    def disable(self, passcode: str, otp: str, features: List[str]) -> TotpDisableResponse:
        api = TotpDisableApi(host=self.host, _session=self.session)
        data = TotpDisableRequestData(
            otp=otp,
            features=features,
            passcode=passcode,
        ).dict(exclude_none=True)

        response = api.call(json=data)
        return TotpDisableResponse.parse_raw(b=response.content)

    def show(self) -> TotpShowResponse:
        api = TotpShowApi(host=self.host, _session=self.session)

        response = api.call()
        return TotpShowResponse.parse_raw(b=response.content)
