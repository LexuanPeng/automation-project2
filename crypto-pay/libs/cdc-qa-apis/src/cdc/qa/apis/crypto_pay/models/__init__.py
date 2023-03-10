from typing import Any, Optional, Type, TypeVar

import urllib3
from requests.auth import AuthBase

from cdc.qa.apis.common.models.rest_api import RestApi
from cdc.qa.apis.common.services.rest_service import RestService
from dataclasses import dataclass, field

from pydantic import BaseModel, ValidationError, Field
from pydantic.error_wrappers import ErrorWrapper

Model = TypeVar("Model", bound="FrozenBaseModel")


@dataclass(frozen=True)
class PayRestApi(RestApi):
    def __post_init__(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@dataclass(frozen=True)
class PayServerService(RestService):
    host: str = field(default="https://pay.3ona.co/api/")


@dataclass(frozen=True)
class PayDashBoardService(RestService):
    host: str = "https://pay.3ona.co/graphql"


@dataclass(frozen=True)
class PayOpsService(RestService):
    host: str = "https://pay.3ona.co/ops/graphql"


class FrozenBaseModel(BaseModel):
    class Config:
        frozen = True

    @classmethod
    def parse_raw(cls: Type[Model], b, **kwargs) -> Model:
        try:
            return super(FrozenBaseModel, cls).parse_raw(b, **kwargs)
        except ValidationError as e:
            errors = e.raw_errors
            errors.append(ErrorWrapper(ValueError(b), loc="original content:"))
            raise ValidationError(errors, model=cls) from None


class GqlRequest(FrozenBaseModel):
    query: str = Field()
    variables: Optional[Any] = Field()


class GqlResponse(FrozenBaseModel):
    data: Optional[Any] = Field()


class BearerPKAuth(AuthBase):
    def __init__(self, pk_key):
        self.pk_key = pk_key

    def __call__(self, r):
        r.headers["Authorization"] = f"Bearer {self.pk_key}"
        r.headers["Content-Type"] = "application/json"
        return r
