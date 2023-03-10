from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.firebase_remote_config.models import FirebaseRemoteConfigRestApi, FirebaseRemoteConfigRestService
from cdc.qa.apis.firebase_remote_config.models.config import RemoteConfigGetResponse


class RemoteConfigGetApi(FirebaseRemoteConfigRestApi):
    """Retrieve the current Firebase Remote Config template from server."""

    method = HttpMethods.GET
    response_type = RemoteConfigGetResponse


class ConfigService(FirebaseRemoteConfigRestService):
    def get(self, project_id: str) -> RemoteConfigGetResponse:
        path = f"v1/projects/{project_id}/remoteConfig"
        api = RemoteConfigGetApi(host=self.host, _session=self.session, path=path)

        response = api.call()
        return RemoteConfigGetResponse.parse_raw(b=response.content)
