import hashlib
import hmac
import random
import time
from enum import Enum, IntEnum
from typing import Any, Optional, Type, TypeVar

from pydantic import BaseModel, Field
from pydantic.error_wrappers import ErrorWrapper, ValidationError

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


class DerivativesRequest(BaseModel):
    """Shared request schema."""

    id: int = Field(
        default=None,
        description="Request Identifier. Response message will contain the same id",
        ge=0,
        le=9_223_372_036_854_775_807,
    )
    method: str = Field(description="The method to be invoked")
    params: BaseModel = Field(default=None, description="Parameters for the methods")
    nonce: int = Field(default=None, description="Current timestamp (milliseconds since the Unix epoch)")

    def __init__(self, **data: Any):
        super().__init__(**data)
        if not self.id:
            object.__setattr__(self, "id", random.randrange(0, 9_223_372_036_854_775_807))
        if not self.nonce:
            object.__setattr__(self, "nonce", int(time.time() * 1000))


class DerivativesSignedRequest(DerivativesRequest):
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
                    param_string += ",".join(value)
                elif isinstance(value, Enum):
                    param_string += value.value
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


class ResponseCodes(IntEnum):
    SUCCESS = 0
    NO_POSITION = 201
    ACCOUNT_IS_SUSPENDED = 202
    ACCOUNTS_DO_NOT_MATCH = 203
    DUPLICATE_CLORDID = 204
    DUPLICATE_ORDERID = 205
    INSTRUMENT_EXPIRED = 206
    NO_MARK_PRICE = 207
    INSTRUMENT_NOT_TRADABLE = 208
    INVALID_INSTRUMENT = 209
    INVALID_ACCOUNT = 210
    INVALID_CURRENCY = 211
    INVALID_ORDERID = 212
    INVALID_ORDERQTY = 213
    INVALID_SETTLE_CURRENCY = 214
    INVALID_FEE_CURRENCY = 215
    INVALID_POSITION_QTY = 216
    INVALID_OPEN_QTY = 217
    INVALID_ORDTYPE = 218
    INVALID_EXECINST = 219
    INVALID_SIDE = 220
    INVALID_TIF = 221
    STALE_MARK_PRICE = 222
    NO_CLORDID = 223
    REJ_BY_MATCHING_ENGINE = 224
    EXCEED_MAXIMUM_ENTRY_LEVERAGE = 225
    INVALID_LEVERAGE = 226
    INVALID_SLIPPAGE = 227
    INVALID_FLOOR_PRICE = 228
    INVALID_REF_PRICE = 229
    INSUFFICIENT_QUANTITY_TO_SELL = 236
    ACCOUNT_IS_IN_MARGIN_CALL = 301
    EXCEEDS_ACCOUNT_RISK_LIMIT = 302
    EXCEEDS_POSITION_RISK_LIMIT = 303
    ORDER_WILL_LEAD_TO_IMMEDIATE_LIQUIDATION = 304
    ORDER_WILL_TRIGGER_MARGIN_CALL = 305
    INSUFFICIENT_AVAILABLE_BALANCE = 306
    INVALID_ORDSTATUS = 307
    INVALID_PRICE = 308
    MARKET_IS_NOT_OPEN = 309
    ORDER_PRICE_BEYOND_LIQUIDATION_PRICE = 310
    POSITION_IS_IN_LIQUIDATION = 311
    ORDER_PRICE_GREATER_THAN_LIMITUPPRICE = 312
    ORDER_PRICE_LESS_THAN_LIMITDOWNPRICE = 313
    EXCEEDS_MAX_ORDER_SIZE = 314
    FAR_AWAY_LIMIT_PRICE = 315
    NO_ACTIVE_ORDER = 316
    POSITION_NO_EXIST = 317
    EXCEEDS_MAX_ALLOWED_ORDERS = 318
    EXCEEDS_MAX_POSITION_SIZE = 319
    EXCEEDS_INITIAL_MARGIN = 320
    EXCEEDS_MAX_AVAILABLE_BALANCE = 321
    EXCEEDS_MAX_EXPOSURE_LIMIT = 322
    ACCOUNT_DOES_NOT_EXIST = 401
    ACCOUNT_IS_NOT_ACTIVE = 406
    MARGIN_UNIT_DOES_NOT_EXIST = 407
    MARGIN_UNIT_IS_SUSPENDED = 408
    INVALID_USER = 409
    USER_IS_NOT_ACTIVE = 410
    USER_NO_DERIV_ACCESS = 411
    ACCOUNT_NO_DERIV_ACCESS = 412
    EXCEED_MAXIMUM_EFFECTIVE_LEVERAGE = 501
    INVALID_COLLATERAL_PRICE = 604
    INVALID_MARGIN_CALC = 605
    EXCEED_ALLOWED_SLIPPAGE = 606
    INSUFFICIENT_MARGIN = 609
    INVALID_INPUT = 2020
    BAD_REQUEST = 40001
    UNAUTHORMETHOD_NOT_FOUNDIZED = 40002
    INVALID_REQUEST = 40003
    MISSING_OR_INVALID_ARGUMENT = 40004
    INVALID_DATE = 40005
    DUPLICATE_REQUEST = 40006
    UNAUTHORIZED = 40101
    INVALID_NONCE = 40102
    IP_ILLEGAL = 40103
    USER_TIER_INVALID = 40104
    NOT_FOUND = 40401
    REQUEST_TIMEOUT = 40801
    TOO_MANY_REQUESTS = 42901
    IMMEDIATE_OR_CANCEL = 43004
    POST_ONLY_REJ = 43005
    ERR_INTERNAL = 50001
    # Websocket Termination Codes
    NORMAL_DISCONNECTION = 1000  # Normal disconnection by server, usually when the heartbeat isn't handled properly
    ABNORML_DISCONNECTION = 1006  # Abnormal disconnection


class DerivativesResponse(FrozenBaseModel):
    """Shared response schema."""

    id: Optional[int] = Field(default=None, description="Original request identifier")
    method: Optional[str] = Field(description="Method invoked")
    result: Optional[Any] = Field(description="Result object")
    code: Optional[ResponseCodes] = Field(description="Response code")
    message: Optional[str] = Field(description="For server or error messages")
    original: Optional[str] = Field(description="Original request as a string, for error cases")
    status: Optional[int] = Field(description="status code for error cases")
    error: Optional[str] = Field(description="error message for error cases")
    path: Optional[str] = Field(description="path for error cases")
