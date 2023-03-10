from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.exchange_derivatives.rest.rest_base import DerivativesRestApi, DerivativesRestService

from ..models.insurance import GetInsuranceRequestParams, GetInsuranceResponse


class GetInsuranceApi(DerivativesRestApi):
    """Fetches balance of Insurance Fund for a particular currency."""

    path = "public/get-insurance"
    method = HttpMethods.GET
    request_params_type = GetInsuranceRequestParams
    response_type = GetInsuranceResponse


class InsuranceService(DerivativesRestService):
    def get_insurance(
        self, instrument_name: str = None, count: int = None, start_ts: int = None, end_ts: int = None
    ) -> GetInsuranceResponse:
        """call get-insurance api

        Args:
            instrument_name (str, optional): e.g. USD_Stable_Coin. Defaults to None.
            count (int, optional): Default is 25. Defaults to None.
            start_ts (int, optional): Default timestamp is 1hr ago (Unix timestamp). Defaults to None.
            end_ts (int, optional): Default timestamp is current time (Unix timestamp). Defaults to None.

        Returns:
            GetInsuranceResponse: GetInsuranceResponse
        """
        api = GetInsuranceApi(host=self.host, _session=self.session)
        params = GetInsuranceRequestParams(
            instrument_name=instrument_name, count=count, start_ts=start_ts, end_ts=end_ts
        ).dict(exclude_none=True)
        response = GetInsuranceResponse.parse_raw(b=api.call(params=params).content)

        return response
