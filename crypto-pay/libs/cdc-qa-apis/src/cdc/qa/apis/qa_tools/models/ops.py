from pydantic import Field
from ..base_models import FrozenBaseModel, QAToolResponse, QAToolSignedRequest


class Env(FrozenBaseModel):
    env: str = Field(default="stg")


# Get ops panel Token
class GetOpsPanelTokenRequestData(QAToolSignedRequest):
    method = "main_app/api_get_ops_token"
    params: Env = Field()


class GetOpsPanelTokenResponse(QAToolResponse):
    class Data(FrozenBaseModel):
        opspanel_key: str
        x_csrf_token: str

    data: Data = Field()


# Set ops panel token
class SetOpsTokenEnv(Env):
    opspanel_key: str
    x_csrf_token: str


class SetOpsPanelTokenRequestData(QAToolSignedRequest):
    method = "main_app/api_set_ops_token"
    params: SetOpsTokenEnv = Field()


class SetOpsPanelTokenResponse(QAToolResponse):
    class Data(FrozenBaseModel):
        msg: str

    data: Data = Field()
