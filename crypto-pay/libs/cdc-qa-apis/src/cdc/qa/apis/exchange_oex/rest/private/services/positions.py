from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.exchange_oex.rest.rest_base import ExchangeRestApi, ExchangeRestService

from ..models.positions import (
    GetPositionsRequestBody,
    GetPositionsRequestParams,
    GetPositionsResponse,
    ClosePositionRequestBody,
    ClosePositionRequestParams,
    ClosePositionResponse,
)


class GetPositionsApi(ExchangeRestApi):
    """exchange deriv private deriv get positions"""

    path = "private/get-positions"
    method = HttpMethods.POST
    request_data_type = GetPositionsRequestBody
    response_type = GetPositionsResponse


class ClosePositionApi(ExchangeRestApi):
    """exchange deriv private deriv close position"""

    path = "private/close-position"
    method = HttpMethods.POST
    request_data_type = ClosePositionRequestBody
    response_type = ClosePositionResponse


class PositionsService(ExchangeRestService):
    def get_positions(self, instrument_name: str = None, system_label: str = None) -> GetPositionsResponse:
        """request get positions
        Args:
            instrument_name (str, optional): instrument name, None for allow. Defaults to None.
        Returns:
            response: GetPositionsResponse
        """
        api = GetPositionsApi(host=self.host, _session=self.session)
        payload = GetPositionsRequestBody(
            params=GetPositionsRequestParams(instrument_name=instrument_name, system_label=system_label),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = GetPositionsResponse.parse_raw(b=api.call(data=payload).content)

        return response

    def close_position(
        self,
        instrument_name: str,
        type: str,
        price: str = None,
        system_label: str = None,
    ) -> ClosePositionResponse:
        """request close position
        Args:
            instrument_name (str): instrument name.
            type (str): order type.
            price (str, optional): order price. Defaults to None.
            system_label:
        Returns:
            response: ClosePositionResponse
        """
        api = ClosePositionApi(host=self.host, _session=self.session)
        payload = ClosePositionRequestBody(
            params=ClosePositionRequestParams(
                instrument_name=instrument_name,
                type=type,
                price=price,
                system_label=system_label,
            ),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)
        response = ClosePositionResponse.parse_raw(b=api.call(data=payload).content)

        return response
