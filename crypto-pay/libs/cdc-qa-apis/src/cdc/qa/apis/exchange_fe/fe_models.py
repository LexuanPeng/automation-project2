from pydantic import BaseModel, Field
from pydantic.error_wrappers import ErrorWrapper, ValidationError
import time
import json
from typing import Any, Optional, Type, TypeVar


Model = TypeVar("Model", bound="FrozenBaseModel")


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


class FeExchangeRequest(BaseModel):
    """Shared request schema."""

    securityInfo: str = Field(default=None, description="contains timestamp and meta json string")
    uaTime: str = Field(default=None, description="Time")

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.uaTime:
            object.__setattr__(self, "uaTime", time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        if not self.securityInfo:
            object.__setattr__(self, "securityInfo", json.dumps({"timestamp": self.uaTime, "meta": {}}))


class FeExchangeResponse(FrozenBaseModel):
    """Shared response schema."""

    code: str = Field(description="code")
    msg: Optional[str] = Field(description="For server or error messages")
    data: Optional[dict] = Field()
