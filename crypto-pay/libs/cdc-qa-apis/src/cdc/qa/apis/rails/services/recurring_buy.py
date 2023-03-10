import logging

from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.rails.models import RailsRestService, RailsRestApi
from cdc.qa.apis.rails.models.recurring_buy import (
    RecurringBuySchedulesPreviewRequestData,
    RecurringBuySchedulesPreviewResponse,
    RecurringBuySchedulesRequestData,
    RecurringBuySchedulesResponse,
    RecurringBuyCancelSchedulesRequestData,
    RecurringBuyCancelSchedulesResponse,
    RecurringBuySchedulesOverviewResponse,
    RecurringBuySchedulesTransactionsQueryParams,
    RecurringBuySchedulesTransactionsResponse,
)
from typing import Optional

logger = logging.getLogger(__name__)


class RecurringBuySchedulesPreviewApi(RailsRestApi):
    """Request recurring buy schedule create preview"""

    path = "recurring_buy/schedules/preview"
    method = HttpMethods.POST
    request_data_type = RecurringBuySchedulesPreviewRequestData
    response_type = RecurringBuySchedulesPreviewResponse


class RecurringBuySchedulesApi(RailsRestApi):
    """Create recurring buy schedules"""

    path = "recurring_buy/schedules"
    method = HttpMethods.POST
    response_type = RecurringBuySchedulesResponse


class RecurringBuyCancelSchedulesApi(RailsRestApi):
    """Cancel recurring buy schedules"""

    path = "recurring_buy/schedules/cancel"
    method = HttpMethods.POST
    response_type = RecurringBuyCancelSchedulesResponse


class RecurringBuySchedulesOverviewApi(RailsRestApi):
    """Get user recurring buy schedules overview"""

    path = "recurring_buy/schedules/overview"
    method = HttpMethods.GET
    response_type = RecurringBuySchedulesOverviewResponse


class RecurringBuySchedulesTransactionsApi(RailsRestApi):
    """Get user recurring buy schedules overview"""

    path = "recurring_buy/transactions"
    method = HttpMethods.GET
    request_params_type = RecurringBuySchedulesTransactionsQueryParams
    response_type = RecurringBuySchedulesTransactionsResponse


class RecurringBuyService(RailsRestService):
    def request_recurring_buy_schedules_preview(
        self,
        amount: str,
        payment_type: str,
        repeat_on: str,
        buy_currency: str,
        sell_currency: str,
        time_zone: str,
        fixed_side: str,
        frequency: str,
    ) -> RecurringBuySchedulesPreviewResponse:
        api = RecurringBuySchedulesPreviewApi(host=self.host, _session=self.session)
        data = RecurringBuySchedulesPreviewRequestData(
            amount=amount,
            payment_type=payment_type,
            repeat_on=repeat_on,
            buy_currency=buy_currency,
            sell_currency=sell_currency,
            time_zone=time_zone,
            fixed_side=fixed_side,
            frequency=frequency,
        ).dict(exclude_none=True)

        response = api.call(data=data)
        return RecurringBuySchedulesPreviewResponse.parse_raw(b=response.content)

    def create_recurring_buy_schedules(
        self,
        amount: str,
        passcode: str,
        payment_type: str,
        repeat_on: str,
        buy_currency: str,
        sell_currency: str,
        time_zone: str,
        fixed_side: str,
        frequency: str,
        specific_weekday: Optional[str] = None,
        specific_week: Optional[str] = None,
    ):
        api = RecurringBuySchedulesApi(host=self.host, _session=self.session)
        data = RecurringBuySchedulesRequestData(
            amount=amount,
            passcode=passcode,
            payment_type=payment_type,
            repeat_on=repeat_on,
            buy_currency=buy_currency,
            sell_currency=sell_currency,
            time_zone=time_zone,
            fixed_side=fixed_side,
            frequency=frequency,
            specific_weekday=specific_weekday,
            specific_week=specific_week,
        ).dict(exclude_none=True)
        response = api.call(json=data)
        recurring_buy_schedules_response = RecurringBuySchedulesResponse.parse_raw(b=response.content)
        logger.debug(f"Recurring buy schedule created: id={recurring_buy_schedules_response.schedule.id}")
        return recurring_buy_schedules_response

    def cancel_recurring_buy_schedules(
        self, schedule_id: str, confirmation_name: str
    ) -> RecurringBuyCancelSchedulesResponse:
        api = RecurringBuyCancelSchedulesApi(host=self.host, _session=self.session)
        data = RecurringBuyCancelSchedulesRequestData(
            schedule_id=schedule_id, confirmation_name=confirmation_name
        ).dict(exclude_none=True)
        response = api.call(json=data)
        logger.debug(f"Recurring buy schedule cancelled: id={schedule_id}")
        return RecurringBuyCancelSchedulesResponse.parse_raw(b=response.content)

    def get_recurring_buy_schedules_overview(self) -> RecurringBuySchedulesOverviewResponse:
        api = RecurringBuySchedulesOverviewApi(host=self.host, _session=self.session)

        response = api.call()
        return RecurringBuySchedulesOverviewResponse.parse_raw(b=response.content)

    def transactions(self, schedule_id: str = None) -> RecurringBuySchedulesTransactionsResponse:
        api = RecurringBuySchedulesTransactionsApi(host=self.host, _session=self.session)
        params = RecurringBuySchedulesTransactionsQueryParams(schedule_id=schedule_id).dict(exclude_none=True)

        response = api.call(params=params)
        return RecurringBuySchedulesTransactionsResponse.parse_raw(b=response.content)
