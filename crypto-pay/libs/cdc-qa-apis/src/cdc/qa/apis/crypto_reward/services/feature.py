from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.crypto_reward.models import CryptoRewardRestApi, CryptoRewardRestService
from cdc.qa.apis.crypto_reward.models.feature import FeatureStatusResponse


class FeatureStatusApi(CryptoRewardRestApi):
    """Show Crypto Reward Feature Status."""

    path = "feature/status"
    method = HttpMethods.GET
    response_type = FeatureStatusResponse


class FeatureStatusService(CryptoRewardRestService):
    def feature_status(self) -> FeatureStatusResponse:
        api = FeatureStatusApi(host=self.host, _session=self.session)

        response = api.call()
        return FeatureStatusResponse.parse_raw(b=response.content)

    def get_reward_flag_status(self) -> bool:
        return self.feature_status().data.reward_flag
