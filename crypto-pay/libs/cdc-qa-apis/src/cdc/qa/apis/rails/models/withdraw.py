from typing import List, Optional, Union
from cdc.qa.apis.rails import RailsResponse
from cdc.qa.apis.rails.models import FrozenBaseModel, RailsEncryptedPasscodeRequest
from cdc.qa.apis.rails.models.common import Balance, Transaction

from pydantic import Field


# --------------------------------- WithdrawalAddPayString --------------------------------- #
class WithdrawalWhitelistAddPayStringRequest(RailsEncryptedPasscodeRequest):
    otp: str = Field()
    pay_id: str = Field()


class WithdrawalWhitelistAddPayStringResponse(RailsResponse):
    ok: bool


# --------------------------------- WithdrawalAddress --------------------------------- #


class TravelRuleWalletType(FrozenBaseModel):
    id: Optional[str]
    name: Optional[str]


class WithdrawalAddress(FrozenBaseModel):
    id: int
    label: str
    currency: str
    address: str
    status: str
    created_at: str
    updated_at: str
    network_id: str
    travel_rule_wallet_type: TravelRuleWalletType
    travel_rulerecipient_name: Optional[str]


class WithdrawalAddressCreateRequestData(RailsEncryptedPasscodeRequest):
    currency: str
    address: str
    label: str
    network_id: str
    otp: Optional[str]
    travel_rule_recipient_name: Optional[str]


class WithdrawalAddressCreateResponse(RailsResponse):
    pending_withdrawal_address: WithdrawalAddress = Field()


class WithdrawalAddressesPathParams(FrozenBaseModel):
    currency: str


class WithdrawalAddressesResponse(RailsResponse):
    addresses: List[WithdrawalAddress] = Field()


# --------------------------------- WithdrawalLimit --------------------------------- #


class WithdrawalLimit(FrozenBaseModel):
    currency: str
    minimum: Balance
    maximum_24h: Balance


class WithdrawalLimitQueryParams(FrozenBaseModel):
    currency: str
    network_id: str


class WithdrawalLimitResponse(RailsResponse):
    limit: WithdrawalLimit = Field()


# --------------------------------- WithdrawalFee --------------------------------- #


class WithdrawalFee(FrozenBaseModel):
    amount: Balance
    native_amount: Balance
    percentage: Optional[str]
    apple_pay_percentage: Optional[str]
    google_pay_percentage: Optional[str]
    network_id: str


class WithdrawalFeeQueryParams(FrozenBaseModel):
    currency: str
    network_id: str
    amount: str


class WithdrawalFeeResponse(RailsResponse):
    fee: WithdrawalFee = Field()


# --------------------------------- WithdrawalCreate --------------------------------- #


class WithdrawalCreateRequestData(RailsEncryptedPasscodeRequest):
    class TravelRuleWalletType(FrozenBaseModel):
        id: int
        name: Optional[str]

    amount: Union[int, str]
    address: str
    currency: str
    network_id: str
    otp: Optional[str]
    phone_otp: Optional[str]
    travel_rule_recipient_name: Optional[str]
    to_wallet_app: Optional[str]
    travel_rule_wallet_type: Optional[TravelRuleWalletType]
    biometric: Optional[bool]
    note: Optional[str]


class WithdrawalCreateResponse(RailsResponse):
    transaction: Transaction = Field()
