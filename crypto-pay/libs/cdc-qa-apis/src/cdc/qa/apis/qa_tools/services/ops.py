from cdc.qa.apis.common.models.rest_api import HttpMethods
from . import QAToolRestApi, QAToolRestService
from ..models.ops import (
    GetOpsPanelTokenRequestData,
    GetOpsPanelTokenResponse,
    Env,
    SetOpsPanelTokenRequestData,
    SetOpsPanelTokenResponse,
    SetOpsTokenEnv,
)


class GetOpsPanelTokenApi(QAToolRestApi):
    path = "tools/v1/main_app/api_get_ops_token/"
    method = HttpMethods.POST
    request_data_type = GetOpsPanelTokenRequestData
    response_type = GetOpsPanelTokenResponse


class SetOpsPanelTokenApi(QAToolRestApi):
    path = "tools/v1/main_app/api_set_ops_token/"
    method = HttpMethods.POST
    request_data_type = SetOpsPanelTokenRequestData
    response_type = SetOpsPanelTokenResponse


class OpsService(QAToolRestService):
    def get_ops_panel_token(self, env: str = "stg") -> GetOpsPanelTokenResponse:
        api = GetOpsPanelTokenApi(host=self.host, _session=self.session)
        data = GetOpsPanelTokenRequestData(
            params=Env(env=env),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)

        response = api.call(data=data)
        return GetOpsPanelTokenResponse.parse_raw(b=response.content)

    def set_ops_panel_token(self, opspanel_key: str, x_csrf_token: str, env: str = "stg") -> SetOpsPanelTokenResponse:
        api = GetOpsPanelTokenApi(host=self.host, _session=self.session)
        data = SetOpsPanelTokenRequestData(
            params=SetOpsTokenEnv(env=env, opspanel_key=opspanel_key, x_csrf_token=x_csrf_token),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)

        response = api.call(data=data)
        return SetOpsPanelTokenResponse.parse_raw(b=response.content)
