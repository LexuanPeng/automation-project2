from typing import List
from cdc.qa.apis.rails import RailsResponse
from cdc.qa.apis.rails.models import FrozenBaseModel, RailsEncryptedPasscodeRequest
from cdc.qa.apis.rails.models.common import Balance

# --------------------------------- SuperchargerAccount --------------------------------- #


class SuperchargerAccountResponse(RailsResponse):
    class Account(FrozenBaseModel):
        class SuperchargerBalance(FrozenBaseModel):
            currency: str
            balance: Balance
            native_balance: Balance

        total_balance: Balance
        balances: List[SuperchargerBalance]
        total_reward: Balance
        percentage_change: str
        is_virgin: bool
        exchange_activated: bool

    supercharger_account: Account


# --------------------------------- SuperchargerEvents --------------------------------- #
class SuperchargerEvent(FrozenBaseModel):
    id: str
    name: str
    status: str
    short_description: str
    end_time: str
    start_time: str
    reward_period_start_time: str
    reward_period_end_time: str
    acceptance_start_time: str
    apy: str
    has_special_apy: bool
    total_distribution: str
    balances: List[Balance]
    total_native_balance: Balance


class SuperchargerEventsQueryParams(FrozenBaseModel):
    is_completed: int


class SuperchargerEventsResponse(RailsResponse):
    events: List[SuperchargerEvent]


# --------------------------------- SuperchargerDepositTerms --------------------------------- #
class SuperchargerDepositTermsRequestData(FrozenBaseModel):
    accepted: bool


class SuperchargerDepositTermsResponse(RailsResponse):
    pass


# --------------------------------- SuperchargerDepositOrders --------------------------------- #
class SuperchargerDepositOrdersCreateRequestData(FrozenBaseModel):
    currency: str
    event_id: str
    amount: str


class SuperchargerDepositOrdersCreateResponse(RailsResponse):
    class DepositOrder(FrozenBaseModel):
        id: str
        user_uuid: str
        amount: Balance
        event_id: str
        event_name: str
        native_amount: Balance
        created_at: str
        updated_at: str

    supercharger_deposit_order: DepositOrder


# --------------------------------- SuperchargerDeposits --------------------------------- #
class SuperchargerDepositsCreateRequestData(RailsEncryptedPasscodeRequest):
    supercharger_deposit_order_id: str


class SuperchargerDepositsCreateResponse(RailsResponse):
    class Deposit(FrozenBaseModel):
        id: str
        user_uuid: str
        status: str
        amount: Balance
        event_id: str
        event_name: str
        native_amount: Balance
        completed_at: str
        created_at: str
        updated_at: str

    supercharger_deposit: Deposit


# --------------------------------- SuperchargerWithdrawalOrders --------------------------------- #
class SuperchargerWithdrawalOrdersCreateRequestData(FrozenBaseModel):
    currency: str
    event_id: str
    amount: str


class SuperchargerWithdrawalOrdersCreateResponse(RailsResponse):
    class WithdrawalOrder(FrozenBaseModel):
        id: str
        user_uuid: str
        amount: Balance
        event_id: str
        event_name: str
        native_amount: Balance
        created_at: str
        updated_at: str

    supercharger_withdrawal_order: WithdrawalOrder


# --------------------------------- SuperchargerWithdrawals --------------------------------- #
class SuperchargerWithdrawalsCreateRequestData(RailsEncryptedPasscodeRequest):
    supercharger_withdrawal_order_id: str


class SuperchargerWithdrawalsCreateResponse(RailsResponse):
    class Withdrawal(FrozenBaseModel):
        id: str
        user_uuid: str
        status: str
        amount: Balance
        event_id: str
        event_name: str
        native_amount: Balance
        completed_at: str
        created_at: str
        updated_at: str

    supercharger_withdrawal: Withdrawal
