from datetime import datetime

from cdc.qa.apis.rails import RailsResponse
from cdc.qa.apis.rails.models import FrozenBaseModel, RailsEncryptedPasscodeRequest
from typing import List, Optional

from cdc.qa.apis.rails.models.common import Balance
from pydantic import Field


# MCOLockupPlans
class MCOLockupPlansResponse(RailsResponse):
    class Plan(FrozenBaseModel):
        class LoungeAccess(FrozenBaseModel):
            enable: bool
            guest_number: int

        class Reimbursement(FrozenBaseModel):
            name: str
            description: str
            logo: str
            cap_amount: Balance
            cap_period: str
            reimbursement_rate: str
            category: str
            eligible: bool

        id: str
        required_fiat_amount: Balance
        lock_amount: Balance
        lock_period_in_days: int
        alternative_payment_methods: List[str]
        mco_stake_reward_apr: str
        staking_currency_rewards_apr: str
        lounge_access: LoungeAccess
        mco_private: bool
        best_rate_in_credit_and_earn: bool
        crypto_earn_extra_mco: str
        reimbursements: List[Reimbursement]
        is_popular: bool
        is_focus: bool

    plans: List[Plan] = Field()


class MCOLockupLockBase(FrozenBaseModel):
    id: str
    user_uuid: str
    current_plan_id: str
    plan_id: str
    payment_method: str
    payment_amount: Balance
    fee_amount: Balance
    lock_amount: Balance
    current_locked_amount: Balance
    required_fiat_amount: Balance
    rate: str
    lock_native_amount: Balance
    current_locked_native_amount: Balance
    total_payment_amount: Balance


# MCOLockupLockOrdersCreate
class MCOLockupLockOrdersCreateRequestData(FrozenBaseModel):
    lock_card_reservation: bool = True
    payment_method: str = "crypto_wallet"
    plan_id: str


class MCOLockupLockOrdersCreateResponse(RailsResponse):
    class MCOLockupLockOrder(MCOLockupLockBase):
        total_payment_amount_in_required_fiat_currency: Balance
        expired_at: datetime
        countdown: int
        purchase_quotation: Optional[str]

    mco_lockup_lock_order: MCOLockupLockOrder = Field()


# MCOLockupLock
class MCOLockupLockRequestData(RailsEncryptedPasscodeRequest):
    order_id: str


class MCOLockupLockResponse(RailsResponse):
    class MCOLockupLock(MCOLockupLockBase):
        status: str

    mco_lockup_lock: MCOLockupLock = Field()
