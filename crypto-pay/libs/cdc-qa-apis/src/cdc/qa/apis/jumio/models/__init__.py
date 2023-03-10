from pydantic import BaseModel
from dataclasses import dataclass

from cdc.qa.apis.common.models.rest_api import RestApi
from cdc.qa.apis.common.services.rest_service import RestService


class FrozenBaseModel(BaseModel):
    class Config:
        frozen = True


@dataclass(frozen=True)
class JumioRestApi(RestApi):
    pass


@dataclass(frozen=True)
class JumioRestService(RestService):
    pass
