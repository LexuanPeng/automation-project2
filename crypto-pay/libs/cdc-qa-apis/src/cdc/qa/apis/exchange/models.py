import hashlib
import hmac
import json
import time
from decimal import Decimal
from enum import IntEnum, Enum
from typing import Any, Optional, Type, TypeVar
from functools import partial

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


class ExchangeRequest(BaseModel):
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
        if not self.nonce:
            object.__setattr__(self, "nonce", int(time.time() * 1000))
        if not self.id:
            object.__setattr__(self, "id", self.nonce)


class ExchangeSignedRequest(ExchangeRequest):
    """Shared signed request schema."""

    api_key: str = Field(description="API key")
    secret_key: str = Field(description="Secret key")
    sig: str = Field(default=None, description="Digital signature")

    def params_to_str(self, obj, level):
        max_level = 3
        if level >= max_level:
            return str(obj)

        if obj is None:
            return "null"
        if isinstance(obj, str):
            return obj
        if isinstance(obj, Enum):
            return obj.value

        if isinstance(obj, dict):
            return_str = ""
            sorted_obj = sorted(obj.items())
            for key, value in sorted_obj:
                return_str += key

                if value is None:
                    return_str += "null"
                else:
                    return_str += self.params_to_str(value, ++level)
            return return_str

        if isinstance(obj, list):
            return "".join([self.params_to_str(sub_obj, ++level) for sub_obj in obj])

        return str(obj)

    def sign(self) -> str:
        param_string = ""

        if self.params:
            param_string = self.params_to_str(self.params.dict(exclude_none=True, by_alias=True), 0)
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
    FEE_ALT_CCY = 1
    PARTIAL_SUCCESS = 10000
    SYS_ERROR = 10001
    UNAUTHORIZED = 10002
    IP_ILLEGAL = 10003
    BAD_REQUEST = 10004
    USER_TIER_INVALID = 10005
    TOO_MANY_REQUESTS = 10006
    INVALID_NONCE = 10007
    METHOD_NOT_FOUND = 10008
    INVALID_DATE_RANGE = 10009
    FAIL = 10010
    DUPLICATE_RECORD = 20001
    NEGATIVE_BALANCE = 20002
    INVALID_JOURNAL_SEQ = 20003
    ACCOUNT_NOT_TRADABLE = 20004
    ACCOUNT_NOT_FOUND = 20005
    JOURNAL_TOTAL_NOT_ZERO = 20006
    USER_NOT_FOUND = 30001
    SYMBOL_NOT_FOUND = 30003
    SIDE_NOT_SUPPORTED = 30004
    ORDERTYPE_NOT_SUPPORTED = 30005
    MIN_PRICE_VIOLATED = 30006
    MAX_PRICE_VIOLATED = 30007
    MIN_QUANTITY_VIOLATED = 30008
    MAX_QUANTITY_VIOLATED = 30009
    MISSING_ARGUMENT = 30010
    EXCHANGE_UNAVAILABLE = 30011
    OMS_ERROR = 30012
    INVALID_PRICE_PRECISION = 30013
    INVALID_QUANTITY_PRECISION = 30014
    MIN_NOTIONAL_VIOLATED = 30016
    MAX_NOTIONAL_VIOLATED = 30017
    INSTRUCTION_SEND_ERROR = 30018
    INSTRUCTION_NO_RESPONSE = 30019
    TOO_MANY_ORDERS = 30021
    BK_UNAVAILABLE = 30020
    ROUTE_ORDER_ERROR = 30022
    MIN_AMOUNT_VIOLATED = 30023
    MAX_AMOUNT_VIOLATED = 30024
    AMOUNT_PRECISION_OVERFLOW = 30025
    OVER_DAILY_LIMIT = 30027
    MG_INVALID_ACCOUNT_STATUS = 40001
    MG_TRANSFER_ACTIVE_LOAN = 40002
    MG_INVALID_LOAN_CURRENCY = 40003
    MG_INVALID_REPAY_AMOUNT = 40004
    MG_NO_ACTIVE_LOAN = 40005
    MG_BLOCKED_BORROW = 40006
    MG_BLOCKED_NEW_ORDER = 40007
    MG_TRANSFER_MARGIN_LEVEL = 40008
    MG_BORROW_MARGIN_LEVEL = 40009
    MG_LEVERAGE_NOT_SUPPORTED = 40010
    MG_LEVERAGE_ADJUSTMENT_REJECTED = 40011
    MG_OPERATION_REJECTED = 40012
    MG_PARAMETERS_INVALID = 40013
    MG_LEVERAGE_ADJUST_REJECTED_GLOBAL_BORROW_LIMIT_REACHED = 40014
    MG_LEVERAGE_ADJUST_REJECTED_COIN_MAX_BORROW_LIMIT_REACHED = 40015
    MG_LEVERAGE_ADJUST_REJECTED_MARGIN_SCORE_IS_AT_OR_BELOW_HAIRCUT = 40016
    MG_LEVERAGE_ADJUST_REJECTED_SUB_ACCOUNT_LEVERAGE = 40017
    MG_BORROW_REJECTED_GLOBAL_BORROW_LIMIT_REACHED = 40018
    MG_BORROW_REJECTED_COIN_MAX_BORROW_LIMIT_REACHED = 40019
    MG_BORROW_REJECTED_MARGIN_SCORE_IS_AT_OR_BELOW_HAIRCUT = 40020
    WEIGHTED_MS_IS_AT_OR_BELOW_HAIRCUT = 40021
    WS_UNAUTHORIZED = 40101
    DW_CREDIT_LINE_NOT_MAINTAINED = 50001
    LEND_INVALID_ACCOUNT_STATUS = 60001
    LEND_INVALID_LOAN_CURRENCY = 60002
    LEND_INVALID_REPAY_AMOUNT = 60003
    LEND_NO_ACTIVE_LOAN = 60004
    LEND_BLOCKED_BORROW = 60005
    LEND_BORROW_REQUEST_LTV_DEVIATED = 60006
    SOURCE_OF_FUND_IS_INVALID = 60007
    USE_OF_LOAN_IS_INVALID = 60008
    TOO_MANY_ACTIVE_LOANS = 60009
    REF_PRICE_ERROR = 60010
    INITIAL_LTV_ERROR = 60011
    MARGIN_CALL_LTV_ERROR = 60012
    LIQUIDATION_LTV_ERROR = 60013
    APR_ERROR = 60014
    LOAN_NOT_FOUND = 60015
    LOAN_IS_UNDER_LIQUIDATION = 60016
    LEND_TC_NOT_ACCEPT = 60017
    LEND_TERM_LENGTH_IS_INVALID = 60018
    LOAN_IS_UNDER_MARGIN_CALL = 60020
    LOAN_INVALID_COLLATERAL_ADJUSTMENT = 60021
    DERIV_EXCEEDS_MAX_AVAILABLE_BALANCE = 70006
    OTC_QUOTE_NOT_FOUND = 91006
    OTC_QUOTE_EXPIRED_ALREADY = 91007
    OTC_GET_QUOTE_ERROR = 91011
    OTC_MAX_AMOUNT_VIOLATED = 91015


class ExchangeResponse(FrozenBaseModel):
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
