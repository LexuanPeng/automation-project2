from typing import Optional, List

from cdc.qa.apis.rails import RailsResponse
from cdc.qa.apis.rails.models import FrozenBaseModel, RailsEncryptedPasscodeRequest
from pydantic import Field, validator
from .common import Balance, Transaction


# --------------------------------- CryptoCreditTerms --------------------------------- #
class StackedMcoTiers(FrozenBaseModel):
    apr: str
    lockup_plans: List[str]


class LoanChoices(FrozenBaseModel):
    currency: str
    max_fraction: int
    min_amount: Balance
    max_amount: Balance


class CryptoCreditTerms(FrozenBaseModel):
    id: str
    collateral_currency: str
    ltv: str
    loan_choices: List[LoanChoices]
    basic_apr: str
    staked_mco_tiers: List[StackedMcoTiers]


# CryptoCreditTerms
class CryptoCreditTermsResponse(RailsResponse):
    crypto_credit_terms: List[CryptoCreditTerms] = Field()


# --------------------------------- CryptoCreditProgramOrder --------------------------------- #
class CryptoCreditProgramOrderRequestData(FrozenBaseModel):
    loan_amount: str = Field()
    payment_type: str = Field()
    term_id: str = Field()
    loan_currency: str = Field()
    payment_currency: str = Field()

    @validator("loan_currency")
    def loan_currency_must_upper_case(cls, v):
        if not v.isupper():
            v = v.upper()
        return v

    @validator("payment_currency")
    def payment_currency_must_upper_case(cls, v):
        if not v.isupper():
            v = v.upper()
        return v


class CryptoCreditProgramOrderResponse(RailsResponse):
    class CryptoCreditProgramOrder(FrozenBaseModel):
        id: str
        collateral_amount: Balance
        collateral_native_amount: Balance
        loan_amount: Balance
        expire_at: str
        countdown: int
        current_apr: str

    crypto_credit_program_order: CryptoCreditProgramOrder = Field()


# --------------------------------- CryptoCreditProgram --------------------------------- #
class CryptoCreditProgramRequestData(RailsEncryptedPasscodeRequest):
    order_id: str = Field()


class CryptoCreditProgram(FrozenBaseModel):
    class CollateralHealthLevels(FrozenBaseModel):
        zone: str
        above_ltv: str
        below_ltv: Optional[str]
        collateral_health: str

    class Rebalance(FrozenBaseModel):
        collateral_amount: Balance
        loan_amount: Balance

    id: str
    collateral_amount: Balance
    collateral_native_amount: Balance
    loan_amount: Balance
    collateral_health: str
    collateral_health_zone: str
    collateral_health_levels: List[CollateralHealthLevels]
    collateral_health_calculating: bool
    current_apr: str
    current_daily_fee: Balance
    rebalance: Rebalance
    term: CryptoCreditTerms


class CryptoCreditProgramResponse(RailsResponse):
    crypto_credit_program: CryptoCreditProgram


# Crypto Credit Account
class CryptoCreditAccount(FrozenBaseModel):
    outstanding_balance: Balance
    percentage_change: str
    is_virgin: bool
    recently_liquidated: bool
    program_creation_paused: bool
    programs: List[CryptoCreditProgram]


class CryptoCreditAccountShowResponse(RailsResponse):
    crypto_credit_account: CryptoCreditAccount


# Crypto credit order create
class CryptoCreditRePaymentOrderRequestData(FrozenBaseModel):
    payment_type: str
    currency: str
    amount: str
    program_id: str
    payment_currency: str


class CryptoCreditRePaymentOrderResponse(RailsResponse):
    class Order(FrozenBaseModel):
        id: str
        payment_type: str
        payment_currency: str
        repayment_amount: Balance
        remain_outstanding_balance: Balance
        countdown: str

    crypto_credit_repayment_order: Order


# Crypto credit repayment create
class CryptoCreditRePaymentCreateRequestData(CryptoCreditProgramRequestData):
    pass


class CryptoCreditRePaymentCreateResponse(RailsResponse):
    class Repayment(FrozenBaseModel):
        apr: str
        repayment_amount: Balance
        principle_paid: Balance
        interest_paid: Balance

    crypto_credit_repayment: Repayment


# Crypto credit transaction
class CryptoCreditTransactionResponse(RailsResponse):
    crypto_credit_transactions: List[Transaction]
