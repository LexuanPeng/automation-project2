from cdc.qa.apis.common.models.rest_api import HttpMethods

from ..fe_base import FeExchangeApi, FeExchangeRestService
from ..models.common import SupportedCoinsResponse, UserInfoRequest, UserInfoResponse


class UserInfoApi(FeExchangeApi):
    path = "common/user_info"
    method = HttpMethods.POST
    request_params_type = UserInfoRequest
    response_type = UserInfoResponse


class SupportedCoinsApi(FeExchangeApi):
    path = "common/supported_coins"
    method = HttpMethods.GET
    response_type = SupportedCoinsResponse


class CommonService(FeExchangeRestService):
    def user_info(self) -> UserInfoResponse:
        """
        Get user info by "common/user_info" API
        :return:
        """
        api = UserInfoApi(host=self.host, _session=self.session, exchange_token=self.exchange_token)
        payload = UserInfoRequest().json(exclude_none=True)
        response = UserInfoResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def supported_coins(self) -> SupportedCoinsResponse:
        """
        Get supported_coins info by "common/supported_coins" API
        :return:
        """
        api = SupportedCoinsApi(host=self.host, _session=self.session, exchange_token=self.exchange_token)
        response = SupportedCoinsResponse.parse_raw(b=api.call().content)
        return response
