from ....models import ExchangeSignedRequest, ExchangeResponse


class AuthRequest(ExchangeSignedRequest):
    method = "public/auth"


class AuthResponse(ExchangeResponse):
    pass
