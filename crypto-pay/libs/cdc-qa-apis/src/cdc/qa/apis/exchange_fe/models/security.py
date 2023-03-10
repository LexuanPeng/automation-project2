from typing import Any, Optional

from pydantic import Field

from ..fe_models import FeExchangeRequest, FeExchangeResponse


# security/send_sms_otp
class SendSMSOTPRequest(FeExchangeRequest):
    pass


class SendSMSOTPResponse(FeExchangeResponse):
    data: Optional[Any] = Field(default=None)
