from typing import Optional, List

from cdc.qa.apis.rails import RailsResponse
from cdc.qa.apis.rails.models import FrozenBaseModel, RailsEncryptedPasscodeRequest
from pydantic import Field, validator
from .common import Balance


# --------------------------------- CryptoEarnTerms --------------------------------- #
class StackedMcoTiers(FrozenBaseModel):
    mco0: str
    mco50: str
    mco500: str
    mco5000: str
    mco50000: str


class DepositCurrencyChoices(FrozenBaseModel):
    currency: str
    extra_interest_currency: Optional[str]
    extra_interest_tiers: Optional[StackedMcoTiers]
    minimum: Balance
    minimum_for_interest: Balance
    staked_mco_tiers: StackedMcoTiers


class CryptoEarnTerms(FrozenBaseModel):
    id: str
    name: str
    description: str
    can_deposit: bool
    period_in_days: int
    period_name: str
    tier2_starts_from: str
    basic_apr: str
    mco_staked_apr: str
    active: bool
    deposit_currency_choices: List[DepositCurrencyChoices]
    is_coming_soon: bool
    is_flexible_term: bool
    term_type: str
    interest_period_in_days: int


# CryptoEarnTerms
class CryptoEarnTermsResponse(RailsResponse):
    crypto_earn_terms: List[CryptoEarnTerms] = Field()


# --------------------------------- CryptoEarnProgramOrder --------------------------------- #
class CryptoEarnProgramOrderRequestData(FrozenBaseModel):
    deposit_amount: str = Field()
    payment_type: str = Field()
    crypto_earn_term_id: str = Field()
    deposit_currency: str = Field()
    program_currency: str = Field()

    @validator("deposit_currency")
    def deposit_currency_must_upper_case(cls, v):
        if not v.isupper():
            v = v.upper()
        return v

    @validator("program_currency")
    def program_currency_must_upper_case(cls, v):
        if not v.isupper():
            v = v.upper()
        return v


class CryptoEarnProgramOrderResponse(RailsResponse):
    class CryptoEarnDepositOrder(FrozenBaseModel):
        id: str
        program_amount: Balance
        program_amount_in_native: Balance
        term_name: str
        apr: str
        extra_interest_currency: Optional[str]
        extra_interest_apr: Optional[str]
        deposit_method: str
        total_cost: Balance
        term_id: str
        term: CryptoEarnTerms
        countdown: int

    crypto_earn_deposit_order: CryptoEarnDepositOrder = Field()


# --------------------------------- CryptoEarnProgram --------------------------------- #
class CryptoEarnProgramRequestData(RailsEncryptedPasscodeRequest):
    payment_type: str = Field()
    crypto_earn_program_order_id: str = Field()
    crypto_earn_term_id: str = Field()
    payment_currency: str = Field()


class CryptoEarnProgram(FrozenBaseModel):
    id: str
    crypto_earn_term_id: str
    crypto_earn_term: CryptoEarnTerms
    principal_asset: Balance
    principal_asset_in_native: Balance
    current_apr: str
    current_extra_apr: Optional[str]
    total_earnings: Balance
    extra_total_earnings: Optional[Balance]
    extra_total_earnings_list: Optional[List[Balance]]
    created_at: str
    will_complete_at: Optional[str]
    current_daily_interest: str
    withdrawn_at: Optional[str]


class CryptoEarnProgramResponse(RailsResponse):
    crypto_earn_program: CryptoEarnProgram = Field()


class CryptoEarnProgramsResponse(RailsResponse):
    crypto_earn_programs: List[CryptoEarnProgram] = Field()


# --------------------------------- CryptoEarnWithdraw --------------------------------- #
class CryptoEarnWithdrawalsCreateRequestData(RailsEncryptedPasscodeRequest):
    amount: str = Field()
    currency: str = Field()
    crypto_earn_program_id: str = Field()


class CryptoEarnWithdrawalsCreateResponse(RailsResponse):
    pass
