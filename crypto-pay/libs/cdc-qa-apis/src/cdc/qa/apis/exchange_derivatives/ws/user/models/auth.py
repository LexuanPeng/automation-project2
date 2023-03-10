from pydantic import validator

from ....models import DerivativesResponse, DerivativesSignedRequest


class AuthRequest(DerivativesSignedRequest):
    method = "public/auth"


class AuthResponse(DerivativesResponse):
    @validator("method")
    def method_match(cls, v):
        assert v == "public/auth", f"method expect:[public/auth] actual:[{v}]!"
        return v
