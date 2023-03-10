from ..fe_base import FeExchangeApi, FeExchangeRestService
from ..models.security import SendSMSOTPRequest, SendSMSOTPResponse
from cdc.qa.apis.common.models.rest_api import HttpMethods


class SendSMSOTPApi(FeExchangeApi):
    path = "security/send_sms_otp"
    method = HttpMethods.POST
    request_data_type = SendSMSOTPRequest
    response_type = SendSMSOTPResponse


class SecurityService(FeExchangeRestService):
    def send_sms_otp(self):
        """
        send sms otp
        :return:
        """
        api = SendSMSOTPApi(host=self.host, _session=self.session, exchange_token=self.exchange_token)
        payload = SendSMSOTPRequest().json(exclude_none=True)
        response = SendSMSOTPResponse.parse_raw(b=api.call(data=payload).content)
        return response
