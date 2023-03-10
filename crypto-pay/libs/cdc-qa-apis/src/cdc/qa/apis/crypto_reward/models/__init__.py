from pydantic import BaseModel, Field
from dataclasses import dataclass
from typing import Optional
from requests.auth import AuthBase
from cdc.qa.apis.common.models.rest_api import RestApi
from cdc.qa.apis.common.services.rest_service import RestService


class FrozenBaseModel(BaseModel):
    class Config:
        frozen = True


@dataclass(frozen=True)
class CryptoRewardRestApi(RestApi):
    pass


@dataclass(frozen=True)
class CryptoRewardRestService(RestService):
    pass


class CryptoRewardResponse(FrozenBaseModel):
    ok: bool = Field()
    error: Optional[str] = Field()


class BearerAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r
