from typing import Any, Optional, Type, TypeVar
from dataclasses import dataclass, field
import requests
from pydantic import Field, BaseModel, ValidationError
from pydantic.error_wrappers import ErrorWrapper

from cdc.qa.apis.common.models.rest_api import RestApi, HttpMethods
from cdc.qa.apis.common.services.rest_service import RestService

Model = TypeVar("Model", bound="FrozenBaseModel")


@dataclass(frozen=True)
class NFTRestApi(RestApi):
    method = HttpMethods.POST
    headers: dict = field(init=False, default_factory=lambda: {"Content-Type": "application/json"})
    nft_token: str = field(default="")

    def __post_init__(self):
        if self.nft_token:
            self.headers["authorization"] = self.nft_token


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


@dataclass(frozen=True)
class NFTRestService(RestService):
    host: str = field()
    nft_token: str = field(default="")
    session: requests.Session = field(default_factory=requests.Session)


class RestRequest(FrozenBaseModel):
    pass


class RestResponse(FrozenBaseModel):
    data: Optional[Any] = Field()
    code: Optional[int] = Field(description="status code for error cases")
    message: Optional[str] = Field(description="execute result message for cases")
    error: Optional[str] = Field(description="error message for error cases")
    errors: Optional[list] = Field()
