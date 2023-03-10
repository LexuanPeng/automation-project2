from . import FrozenBaseModel, RailsEncryptedPasscodeRequest, RailsResponse
from pydantic import Field
from typing import List


# --------------------------------- TotpCreate ------------------------------- #
class TotpCreateRequestData(RailsEncryptedPasscodeRequest):
    pass


class TotpCreateResponse(RailsResponse):
    class Totp(FrozenBaseModel):
        secret: str = Field()
        uri: str = Field()

    totp: Totp = Field()


# --------------------------------- TotpVerify ------------------------------- #
class TotpVerifyRequestData(FrozenBaseModel):
    otp: str = Field()


class TotpVerifyResponse(RailsResponse):
    pass


# --------------------------------- TotpDisable ------------------------------- #
class TotpDisableRequestData(RailsEncryptedPasscodeRequest):
    otp: str = Field()
    features: List[str] = Field()


class TotpDisableResponse(RailsResponse):
    class Totp(FrozenBaseModel):
        status: str
        enabled_features: List[str]

    totp: Totp = Field()


# --------------------------------- TotpShow------------------------------- #
class TotpShowResponse(TotpDisableResponse):
    pass
