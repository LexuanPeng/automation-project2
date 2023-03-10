from pydantic import validator

from ....models import ExchangeRequestParams, ExchangeResponse, ExchangeSignedRequest


class AuthRequest(ExchangeSignedRequest):
    method = "public/auth"
    params: ExchangeRequestParams


class AuthResponse(ExchangeResponse):
    @validator("method")
    def method_match(cls, v):
        assert v == "public/auth", f"method expect:[public/auth] actual:[{v}]!"
        return v
