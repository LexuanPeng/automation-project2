import hashlib
import hmac
import json
import time
from decimal import Decimal
from functools import partial
from typing import Any, Dict, Type, TypeVar

from pydantic import BaseModel, Field
from pydantic.error_wrappers import ErrorWrapper, ValidationError

Model = TypeVar("Model", bound="FrozenBaseModel")


class FrozenBaseModel(BaseModel):
    class Config:
        frozen = True
        json_loads = partial(json.loads, parse_float=Decimal)

    @classmethod
    def parse_raw(cls: Type[Model], b, **kwargs) -> Model:
        try:
            return super(FrozenBaseModel, cls).parse_raw(b, **kwargs)
        except ValidationError as e:
            errors = e.raw_errors
            errors.append(ErrorWrapper(ValueError(b), loc="original content:"))
            raise ValidationError(errors, model=cls) from None


class QAToolRequest(BaseModel):
    """Shared request schema."""

    id: str = Field(default=None, description="Request Identifier. Response message will contain the same id")
    method: str = Field(description="The method to be invoked")
    params: BaseModel = Field(default=None, description="Parameters for the methods")
    nonce: int = Field(default=None, description="Current timestamp (milliseconds since the Unix epoch)")

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.nonce:
            object.__setattr__(self, "nonce", str(int(time.time() * 1000)))
        if not self.id:
            object.__setattr__(self, "id", f"{self.nonce}123000")


class QAToolSignedRequest(QAToolRequest):
    """Shared signed request schema."""

    api_key: str = Field(description="API key")
    secret_key: str = Field(description="Secret key")
    sig: str = Field(default=None, description="Digital signature")

    def sign(self) -> str:
        param_string = ""

        if self.params:
            params = sorted(self.params.dict(exclude_none=True, by_alias=True).items())
            for key, value in params:
                param_string += key
                if value is None:
                    param_string += "null"
                elif isinstance(value, list):
                    if len(value) != 0:
                        value = list(map(lambda x: str(x), value))
                    param_string += ",".join(value)
                else:
                    param_string += str(value)

        sig_payload = f"{self.method}{self.id}{self.api_key}{param_string}{self.nonce}"
        sig = hmac.new(
            bytes(str(self.secret_key), "utf-8"),
            msg=bytes(sig_payload, "utf-8"),
            digestmod=hashlib.sha256,
        ).hexdigest()
        return sig

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.sig:
            object.__setattr__(self, "sig", self.sign())
        object.__delattr__(self, "secret_key")


class QAToolResponse(FrozenBaseModel):
    """Shared response schema."""

    msg: str = Field(description="msg")
    error: Dict = Field(description="error data")
    data: Any = Field(description="data")
