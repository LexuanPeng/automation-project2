from typing import List, Optional

from cdc.qa.apis.rails import RailsResponse
from cdc.qa.apis.rails.models import FrozenBaseModel

from pydantic import Field


# AppFeaturesRequiredPersonalInformation
class AppFeaturesRequiredPersonalInformationResponse(RailsResponse):
    class RequiredPersonalInformation(FrozenBaseModel):
        app_access: Optional[List[str]]
        fiat_withdrawal: Optional[List[str]]
        pay_your_friends: Optional[List[str]]
        crypto_withdrawal: Optional[List[str]]
        deposit_to_ex: Optional[List[str]]
        fiat_to_card_top_up: Optional[List[str]]
        crypto_to_card_top_up: Optional[List[str]]
        eur_crypto_to_fiat: Optional[List[str]]
        eur_fiat_to_crypto: Optional[List[str]]
        eur_to_card_top_up: Optional[List[str]]
        au_npp_account_creation: Optional[List[str]]
        au_bpay_account_creation: Optional[List[str]]
        sepa_account_creation: Optional[List[str]]

    required_personal_information: Optional[RequiredPersonalInformation] = Field()


# App lock
class AppLockShowResponse(RailsResponse):
    class Lock(FrozenBaseModel):
        app_locked: bool
        app_lock_expires_at: str

    app_lock: Lock
