import urllib3
from pydantic import BaseModel, Field
from dataclasses import dataclass
from typing import Optional, List, Union
import logging

from cdc.qa.apis.common.models.rest_api import RestApi
from cdc.qa.apis.common.services.rest_service import RestService


logger = logging.getLogger(__name__)


class FrozenBaseModel(BaseModel):
    class Config:
        frozen = True


class SonicCloudResponse(FrozenBaseModel):
    code: int = Field()
    message: str = Field()
    data: Optional[Union[str, List]] = Field()


class SonicCloudError(Exception):
    pass


@dataclass(frozen=True)
class SonicCloudRestApi(RestApi):
    def __post_init__(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@dataclass(frozen=True)
class SonicCloudService(RestService):
    uuid_key: str = Field()
