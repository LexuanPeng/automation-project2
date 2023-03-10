import urllib3
from pydantic import BaseModel
from dataclasses import dataclass, field

from cdc.qa.apis.common.models.rest_api import RestApi
from cdc.qa.apis.common.services.rest_service import RestService


class FrozenBaseModel(BaseModel):
    class Config:
        frozen = True


@dataclass(frozen=True)
class FirebaseRemoteConfigRestApi(RestApi):
    path: str = field(default="")

    def __post_init__(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@dataclass(frozen=True)
class FirebaseRemoteConfigRestService(RestService):
    pass
