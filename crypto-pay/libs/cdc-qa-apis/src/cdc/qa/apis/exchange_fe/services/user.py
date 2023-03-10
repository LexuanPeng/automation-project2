from ..fe_base import FeExchangeRestService, FeExchangeApi
from ..models.user import (
    UpdateFeeCoinOpenRequest,
    UpdateFeeCoinOpenResponse,
    StakingInfoResponse,
    WithdrawalInfoResponse,
)
from cdc.qa.apis.common.models.rest_api import HttpMethods


class UpdataFeeCoinOpenApi(FeExchangeApi):
    path = "user/update_fee_coin_open"
    method = HttpMethods.POST
    request_params_type = UpdateFeeCoinOpenRequest
    response_type = UpdateFeeCoinOpenResponse


class StakingInfoApi(FeExchangeApi):
    path = "user/staking_info"
    method = HttpMethods.GET
    response_type = StakingInfoResponse


class WithdrawalInfoApi(FeExchangeApi):
    path = "user/withdrawal_info"
    method = HttpMethods.GET
    response_type = WithdrawalInfoResponse


class UserService(FeExchangeRestService):
    def update_fee_coin_open(self, useFeeCoinOpen: str):
        """
        Enable or disable Rebates
        :param useFeeCoinOpen: 1 - enable rebates, 0 - disable rebates
        :return:
        """
        api = UpdataFeeCoinOpenApi(host=self.host, _session=self.session, exchange_token=self.exchange_token)
        payload = UpdateFeeCoinOpenRequest(useFeeCoinOpen=useFeeCoinOpen).json(exclude_none=True)
        response = UpdateFeeCoinOpenResponse.parse_raw(b=api.call(data=payload).content)
        return response

    def staking_info(self):
        """
        get user staking info
        :return:
        """
        api = StakingInfoApi(host=self.host, _session=self.session, exchange_token=self.exchange_token)
        response = StakingInfoResponse.parse_raw(b=api.call().content)
        return response

    def withdrawal_info(self) -> WithdrawalInfoResponse:
        """get user withdrawal info

        Returns:
            WithdrawalInfoResponse: info response
        """
        api = WithdrawalInfoApi(host=self.host, _session=self.session, exchange_token=self.exchange_token)
        response = WithdrawalInfoResponse.parse_raw(b=api.call().content)
        return response
