from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.rails.models.app import AppFeaturesRequiredPersonalInformationResponse, AppLockShowResponse

from ..models import RailsRestApi, RailsRestService


class AppFeaturesRequiredPersonalInformationApi(RailsRestApi):
    """Get lists of required personal information."""

    path = "app/features/required_personal_information"
    method = HttpMethods.GET
    response_type = AppFeaturesRequiredPersonalInformationResponse


class AppLockShowApi(RailsRestApi):
    """Get lists of required personal information."""

    path = "app_lock/show"
    method = HttpMethods.GET
    response_type = AppLockShowResponse


class AppService(RailsRestService):
    def features_required_personal_information(self) -> AppFeaturesRequiredPersonalInformationResponse:
        """Generate OAuth token for user."""
        api = AppFeaturesRequiredPersonalInformationApi(host=self.host, _session=self.session)

        response = api.call()
        return AppFeaturesRequiredPersonalInformationResponse.parse_raw(b=response.content)

    def app_lock_show(self) -> AppLockShowResponse:
        api = AppLockShowApi(host=self.host, _session=self.session)
        response = api.call()

        return AppLockShowResponse.parse_raw(b=response.content)
