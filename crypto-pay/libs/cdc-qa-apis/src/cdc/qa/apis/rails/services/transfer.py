import logging
from typing import Optional

from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.rails.models.transfer import (
    TransferCreateRequestData,
    TransferCreateResponse,
)
from ..models import RailsRestApi, RailsRestService


logger = logging.getLogger(__name__)


class TransferCreateApi(RailsRestApi):
    """Create crypto transfer"""

    path = "crypto_wallets/transfers/create"
    method = HttpMethods.POST
    request_data_type = TransferCreateRequestData
    response_type = TransferCreateResponse


class TransferService(RailsRestService):
    def create_transfer(
        self,
        to_name: str,
        to_phone: str,
        currency: str,
        passcode: str,
        amount: Optional[str],
        native_amount: Optional[str],
        otp: Optional[str],
        phone_otp: Optional[str],
    ) -> TransferCreateResponse:
        # amount or native amount is required
        api = TransferCreateApi(host=self.host, _session=self.session)
        data = TransferCreateRequestData(
            to_name=to_name,
            to_phone=to_phone,
            amount=amount,
            currency=currency,
            passcode=passcode,
            otp=otp,
            phone_otp=phone_otp,
            native_amount=native_amount,
        ).dict(exclude_none=True)

        response = api.call(data=data)
        return TransferCreateResponse.parse_raw(b=response.content)
