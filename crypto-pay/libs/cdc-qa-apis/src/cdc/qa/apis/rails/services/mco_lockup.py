from enum import Enum
from typing import Union

from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.rails.models import RailsRestApi, RailsRestService
from cdc.qa.apis.rails.models.mco_lockup import (
    MCOLockupPlansResponse,
    MCOLockupLockOrdersCreateRequestData,
    MCOLockupLockOrdersCreateResponse,
    MCOLockupLockRequestData,
    MCOLockupLockResponse,
)


class PlanId(Enum):
    blue = "mco0"
    ruby = "mco50"
    jade = "mco500"
    indigo = "mco500"
    white = "mco5000"
    rose = "mco5000"
    black = "mco50000"


class MCOLockupPlansApi(RailsRestApi):
    """Get MCO card lock up plans."""

    path = "mco_lockup/plans"
    method = HttpMethods.GET
    response_type = MCOLockupPlansResponse


class MCOLockupLockOrdersCreateApi(RailsRestApi):
    """Create MCO card lock up order."""

    path = "v2/mco_lockup/lock_orders/create"
    method = HttpMethods.POST
    request_data_type = MCOLockupLockOrdersCreateRequestData
    response_type = MCOLockupLockOrdersCreateResponse


class MCOLockupLockApi(RailsRestApi):
    """Process for the MCO card lock up order."""

    path = "v2/mco_lockup/lock"
    method = HttpMethods.POST
    request_data_type = MCOLockupLockRequestData
    response_type = MCOLockupLockResponse


class MCOLockupService(RailsRestService):
    def plans(self) -> MCOLockupPlansResponse:
        api = MCOLockupPlansApi(host=self.host, _session=self.session)

        response = api.call()
        return MCOLockupPlansResponse.parse_raw(b=response.content)

    def get_mco_card_lock_amount_in_cro(self, mco_card_tier: str) -> int:
        plan_id = PlanId[mco_card_tier].value
        plan = next(filter(lambda x: x.id == plan_id, self.plans().plans))
        return int(plan.lock_amount.amount or 0)

    def stake_mco_card(self, card_tier: str, passcode: Union[str, int]):
        """Stake mco card with CRO."""

        order_id = self._lock_orders_create(PlanId[card_tier].value).mco_lockup_lock_order.id
        return self._lock(order_id, str(passcode))

    def _lock_orders_create(self, plan_id: str) -> MCOLockupLockOrdersCreateResponse:
        api = MCOLockupLockOrdersCreateApi(host=self.host, _session=self.session)
        data = MCOLockupLockOrdersCreateRequestData(plan_id=plan_id).dict(exclude_none=True)

        response = api.call(data=data)
        return MCOLockupLockOrdersCreateResponse.parse_raw(b=response.content)

    def _lock(self, order_id: str, passcode: str) -> MCOLockupLockResponse:
        api = MCOLockupLockApi(host=self.host, _session=self.session)
        data = MCOLockupLockRequestData(order_id=order_id, passcode=passcode).dict(exclude_none=True)

        response = api.call(data=data)
        return MCOLockupLockResponse.parse_raw(b=response.content)
