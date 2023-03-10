from ..fe_base import FeExchangeApi, FeExchangeRestService
from ..models.account import CreateMarginAccountRequest, CreateMarginAccountResponse
from cdc.qa.apis.common.models.rest_api import HttpMethods


class CreateMarginAccountApi(FeExchangeApi):
    path = "create-margin-account"
    method = HttpMethods.POST
    request_params_type = CreateMarginAccountRequest
    response_type = CreateMarginAccountResponse


class AccountService(FeExchangeRestService):
    def create_margin_account(self):
        """
        Open Margin Wallet
        :return:
        """
        api = CreateMarginAccountApi(host=self.host, _session=self.session, exchange_token=self.exchange_token)
        payload = CreateMarginAccountRequest().json(exclude_none=True)
        response = CreateMarginAccountResponse.parse_raw(b=api.call(data=payload).content)
        return response
