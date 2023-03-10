from typing import List, Optional

from cdc.qa.apis.rails import RailsResponse
from cdc.qa.apis.rails.models import FrozenBaseModel, RailsEncryptedPasscodeRequest
from pydantic import Field, validator
from cdc.qa.apis.rails.models.common import Balance, Transaction


class ScheduleView(FrozenBaseModel):
    id: Optional[str]
    sell_currency: str
    buy_currency: str
    amount: str
    fixed_side: str
    start_date: str
    next_execution_time: str
    frequency: str
    status: str
    first_order_executed: bool
    has_pending_order: bool
    created_at: str
    repeat_on: str
    specific_week: Optional[str]
    specific_weekday: Optional[str]


# --------------------------------- RecurringBuySchedulesPreview --------------------------------- #
class RecurringBuySchedulesPreviewRequestData(FrozenBaseModel):
    amount: str = Field()
    payment_type: str = Field()
    repeat_on: str = Field()
    buy_currency: str = Field()
    sell_currency: str = Field()
    time_zone: str = Field()
    fixed_side: str = Field()
    frequency: str = Field()


class RecurringBuySchedulesPreviewResponse(RailsResponse):
    recurring_buy_schedule_view: ScheduleView = Field()


# --------------------------------- RecurringBuySchedules --------------------------------- #
class RecurringBuySchedulesRequestData(RailsEncryptedPasscodeRequest):
    amount: str = Field()
    payment_type: str = Field()
    repeat_on: str = Field()
    buy_currency: str = Field()
    sell_currency: str = Field()
    payment_card_id: Optional[str] = Field()
    time_zone: str = Field()
    fixed_side: str = Field()
    frequency: str = Field()
    specific_weekday: Optional[str] = Field()
    specific_week: Optional[int] = Field()

    @validator("buy_currency")
    def buy_currency_must_upper_case(cls, v):
        if not v.isupper():
            v = v.upper()
        return v

    @validator("sell_currency")
    def sell_currency_must_upper_case(cls, v):
        if not v.isupper():
            v = v.upper()
        return v


class RecurringBuySchedulesResponse(RailsResponse):
    class Schedule(FrozenBaseModel):
        id: str
        user_uuid: str
        buy_currency: str
        sell_currency: str
        amount: str
        fixed_side: str
        start_date: str
        next_execution_time: str
        frequency: str
        repeat_on: str
        specific_week: Optional[str]
        specific_weekday: Optional[str]
        payment_type: str
        payment_card_id: Optional[str]
        status: str
        created_at: str
        updated_at: Optional[str]
        time_zone: str
        cancelled_done_by: Optional[str]
        payment_card: Optional[str]
        ended_at: Optional[str]
        ip_address: str
        ip_country: str

    url: Optional[str] = Field()
    schedule: Optional[Schedule] = Field()


# --------------------------------- RecurringBuyCancelSchedules --------------------------------- #
class RecurringBuyCancelSchedulesRequestData(FrozenBaseModel):
    schedule_id: str = Field()
    confirmation_name: str = Field()


class RecurringBuyCancelSchedulesResponse(RailsResponse):
    pass


# --------------------------------- RecurringBuySchedulesOverview --------------------------------- #
class RecurringBuySchedulesOverviewResponse(RailsResponse):
    class ScheduleOverview(FrozenBaseModel):
        monthly_used: Balance
        monthly_quota: Balance
        schedules: List[ScheduleView]

    schedule_overview: ScheduleOverview = Field()


# --------------------------------- RecurringBuySchedulesTxns --------------------------------- #
class RecurringBuySchedulesTransactionsQueryParams(FrozenBaseModel):
    schedule_id: Optional[str]


class RecurringBuySchedulesTransactionsResponse(RailsResponse):
    transactions: List[Transaction]
