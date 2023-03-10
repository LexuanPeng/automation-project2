from cdc.qa.apis.crypto_reward.models import FrozenBaseModel, CryptoRewardResponse
from pydantic import Field


class FeatureStatusResponse(CryptoRewardResponse):
    class Data(FrozenBaseModel):
        reward_flag: bool
        mission_available: bool
        diamond_redemption_available: bool
        reward_store_items_available: bool
        reward_vault_available: bool

    data: Data = Field()
