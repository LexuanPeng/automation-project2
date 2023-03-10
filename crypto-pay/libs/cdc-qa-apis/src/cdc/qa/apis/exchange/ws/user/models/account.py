from enum import Enum
from typing import List, Optional
from pydantic import Field, validator
from decimal import Decimal
from ...models import SubscribeResponseResult, SubscribeResponse, SubscribeRequest
from ....models import FrozenBaseModel, ExchangeResponse, ExchangeRequest


class UserBalanceDetail(FrozenBaseModel):
    currency: str = Field(description="e.g. CRO")
    balance: Decimal = Field(description="Total balance")
    available: Decimal = Field(description="Available balance (e.g. not in orders, or locked, etc.)")
    order: Decimal = Field(description="Balance locked in orders")
    stake: Decimal = Field(description="Balance locked for staking (typically only used for CRO)")


class SubscribeUserBalanceRequestParams(FrozenBaseModel):
    channels: List[str] = ["user.balance"]


class SubscribeUserBalanceRequest(SubscribeRequest):
    params: SubscribeUserBalanceRequestParams = SubscribeUserBalanceRequestParams()


class SubscribeUserBalanceResponseResult(SubscribeResponseResult):
    channel: str = "user.balance"
    subscription: str = "user.balance"
    data: List[UserBalanceDetail] = Field()

    @validator("channel")
    def channel_match(cls, v):
        assert v == "user.balance", f"channel expect:[user.balance] actual:[{v}]!"
        return v

    @validator("subscription")
    def subscription_match(cls, v):
        assert v == "user.balance", f"subscription expect:[user.balance] actual:[{v}]!"
        return v


class SubscribeUserBalanceResponse(SubscribeResponse):
    result: SubscribeUserBalanceResponseResult = Field(default=None)


class AccountDetail(FrozenBaseModel):
    balance: Decimal = Field(description="Total balance")
    available: Decimal = Field(description="Available balance (e.g. not in orders, or locked, etc.)")
    order: Decimal = Field(description="Balance locked in orders")
    stake: Decimal = Field(description="Balance locked for staking (typically only used for CRO)")
    currency: str = Field(description="e.g. CRO")


# private/get-account-summary
class PrivateGetAccountSummaryRequestParams(FrozenBaseModel):
    currency: Optional[str] = Field(default=None, description="Specific currency, e.g. CRO. Omit for 'all'")


class PrivateGetAccountSummaryRequest(ExchangeRequest):
    method: str = "private/get-account-summary"
    params: PrivateGetAccountSummaryRequestParams = Field()


class PrivateGetAccountSummaryResult(FrozenBaseModel):
    accounts: List[AccountDetail] = Field()


class PrivateGetAccountSummaryResponse(ExchangeResponse):
    result: PrivateGetAccountSummaryResult = Field()

    @validator("method")
    def method_match(cls, v):
        method = "private/get-account-summary"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/create-withdrawal
class PrivateCreateWithdrawalRequestParams(FrozenBaseModel):
    client_wid: Optional[str] = Field(description="Optional Client withdrawal ID")
    currency: str = Field(description="E.g. BTC, CRO")
    amount: Decimal
    address: str = Field(description="Address with Address Tag (if any)")
    address_tag: Optional[str] = Field(
        description="Secondary address identifier for coins like XRP, XLM etc. Also known as memo or tags."
    )


class PrivateCreateWithdrawalRequest(ExchangeRequest):
    method: str = "private/create-withdrawal"
    params: PrivateCreateWithdrawalRequestParams = Field()


class PrivateCreateWithdrawalResult(FrozenBaseModel):
    id: int = Field(description="Newly created withdrawal ID")
    client_wid: Optional[str] = Field(description="(Optional) if a Client withdrawal ID was provided in the request")
    currency: str = Field(description="E.g. BTC, CRO, ETH")
    amount: Decimal
    fee: Decimal
    address: str = Field(description="Address with Address Tag (if any)")
    create_time: int
    network_id: Optional[str]


class PrivateCreateWithdrawalResponse(ExchangeResponse):
    result: PrivateCreateWithdrawalResult = Field()

    @validator("method")
    def method_match(cls, v):
        method = "private/create-withdrawal"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v


# private/get-withdrawal-history
class WithdrawalStatus(Enum):
    """
    0 - Pending
    1 - Processing
    2 - Rejected
    3 - Payment In-progress
    4 - Payment Failed
    5 - Completed
    6 - Cancelled
    """

    PENDING = "0"
    Processing = "1"
    REJECTED = "2"
    PAYMENT_IN_PROGRESS = "3"
    PAYMENT_FAILED = "4"
    COMPLETED = "5"
    CANCELLED = "6"


class PrivateGetWithdrawalHistoryRequestParams(FrozenBaseModel):
    currency: Optional[str] = Field(description="E.g. BTC, CRO")
    start_ts: Optional[int] = Field(description="Default is 90 days from current timestamp")
    end_ts: Optional[str] = Field(description="Default is current timestamp")
    page_size: Optional[int] = Field(description="Page size (Default: 20, Max: 200)")
    page: Optional[int] = Field(description="Page number (0-based)")
    status: Optional[WithdrawalStatus] = Field(description="withdrawal status")


class PrivateGetWithdrawalHistoryRequest(ExchangeRequest):
    method: str = "private/get-withdrawal-history"
    params: PrivateGetWithdrawalHistoryRequestParams = Field()


class WithdrawalDetail(FrozenBaseModel):
    id: int = Field(description="Newly created withdrawal ID")
    client_wid: str = Field(description="(Optional) if a Client withdrawal ID was provided in the request")
    currency: str = Field(description="E.g. BTC, CRO")
    amount: Decimal
    fee: Decimal
    address: str = Field(description="Address with Address Tag (if any)")
    create_time: int
    update_time: int
    status: WithdrawalStatus = Field(description="withdrawal status")
    txid: str = Field(description="Transaction hash")


class PrivateGetWithdrawalHistoryResult(FrozenBaseModel):
    withdrawal_list: List[WithdrawalDetail] = Field()


class PrivateGetWithdrawalHistoryResponse(ExchangeResponse):
    result: PrivateGetWithdrawalHistoryResult = Field()

    @validator("method")
    def method_match(cls, v):
        method = "private/get-withdrawal-history"
        assert v == method, f"check method incorrect. E:{method} A:{v}"
        return v
