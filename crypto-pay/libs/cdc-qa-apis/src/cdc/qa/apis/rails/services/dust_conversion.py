from typing import List
from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.rails.models import RailsRestApi, RailsRestService
from cdc.qa.apis.rails.models.dust_conversion import (
    DustConversionOverviewResponse,
    DustConversionOrderRequestData,
    DustConversionOrderResponse,
    DustConversionCreateRequestData,
    DustConversionCreateResponse,
)


class DustConversionOverviewApi(RailsRestApi):
    """get dust conversion overview"""

    path = "dust_conversion/overview"
    method = HttpMethods.GET
    response_type = DustConversionOverviewResponse


class DustConversionOrderApi(RailsRestApi):
    """create dust conversion order"""

    path = "dust_conversion/orders/create"
    method = HttpMethods.POST
    request_data_type = DustConversionOrderRequestData
    response_type = DustConversionOrderResponse


class DustConversionCreateApi(RailsRestApi):
    """create dust conversion order"""

    path = "dust_conversion/conversions/create"
    method = HttpMethods.POST
    request_data_type = DustConversionCreateRequestData
    response_type = DustConversionCreateResponse


class DustConversionService(RailsRestService):
    def overview(self) -> DustConversionOverviewResponse:
        api = DustConversionOverviewApi(host=self.host, _session=self.session)

        response = api.call()
        return DustConversionOverviewResponse.parse_raw(b=response.content)

    def create_order(self, dust_currencies: List[str], deposit_currency: str) -> DustConversionOrderResponse:
        api = DustConversionOrderApi(host=self.host, _session=self.session)
        data = DustConversionOrderRequestData(dust_currencies=dust_currencies, deposit_currency=deposit_currency).dict(
            exclude_none=True
        )

        response = api.call(json=data)
        return DustConversionOrderResponse.parse_raw(b=response.content)

    def create_conversion(self, order_id: str, passcode: str) -> DustConversionCreateResponse:
        api = DustConversionCreateApi(host=self.host, _session=self.session)
        data = DustConversionCreateRequestData(order_id=order_id, passcode=passcode).dict(exclude_none=True)

        response = api.call(data=data)
        return DustConversionCreateResponse.parse_raw(b=response.content)
