from typing import Optional, List, Union

from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.sonic_cloud.models import SonicCloudRestApi, SonicCloudResponse, SonicCloudService
from cdc.qa.apis.sonic_cloud.models.appium import (
    GetDevicesRequest,
    CloseAppiumSessionQueryParams,
    CreateAppiumSessionQueryParams,
    EndAppiumSessionRequest,
    GetAllDevicesRequest,
    LockDeviceQueryParams,
    ReleaseDeviceQueryParams,
    GetAvailableAppiumPortRequest,
)


class CloseAppiumSessionApi(SonicCloudRestApi):
    """Appium close session callback sonic. Release devices."""

    path = "/server/api/controller/appium/closeAppiumSession"
    method = HttpMethods.GET
    request_params_type = CloseAppiumSessionQueryParams
    response_type = SonicCloudResponse


class CreateAppiumSessionApi(SonicCloudRestApi):
    """Appium created session callback sonic. Lock devices."""

    path = "/server/api/controller/appium/createAppiumSession"
    method = HttpMethods.GET
    request_params_type = CreateAppiumSessionQueryParams
    response_type = SonicCloudResponse


class EndAppiumSessionApi(SonicCloudRestApi):
    """Force end device's appium session."""

    path = "/server/api/controller/appium/endAppiumSession"
    method = HttpMethods.POST
    request_data_type = EndAppiumSessionRequest
    response_type = SonicCloudResponse


class GetAllDevicesApi(SonicCloudRestApi):
    """Get all online devices, all agent devices."""

    path = "/server/api/controller/appium/getAllDevices"
    method = HttpMethods.POST
    request_data_type = GetAllDevicesRequest
    response_type = SonicCloudResponse


class GetDevicesApi(SonicCloudRestApi):
    """Get devices, return appium address."""

    path = "/server/api/controller/appium/getDevices"
    method = HttpMethods.POST
    request_data_type = GetDevicesRequest
    response_type = SonicCloudResponse


class LockDeviceApi(SonicCloudRestApi):
    """Lock the device, do nothing."""

    path = "/server/api/controller/appium/lockDevice"
    method = HttpMethods.POST
    request_params_type = LockDeviceQueryParams
    response_type = SonicCloudResponse


class ReleaseDeviceApi(SonicCloudRestApi):
    """Release the device, do nothing."""

    path = "/server/api/controller/appium/releaseDevice"
    method = HttpMethods.POST
    request_params_type = ReleaseDeviceQueryParams
    response_type = SonicCloudResponse


class GetAvailableAppiumPortApi(SonicCloudRestApi):
    path = "/server/api/controller/appium/getAvailableAppiumPort"
    method = HttpMethods.POST
    request_params_type = GetAvailableAppiumPortRequest
    response_type = SonicCloudResponse


class AppiumService(SonicCloudService):
    def close_appium_session(self) -> SonicCloudResponse:
        api = CloseAppiumSessionApi(host=self.host, _session=self.session)

        response = api.call()
        return SonicCloudResponse.parse_raw(b=response.content)

    def get_all_devices(self) -> SonicCloudResponse:
        api = GetAllDevicesApi(host=self.host, _session=self.session)

        response = api.call()
        return SonicCloudResponse.parse_raw(b=response.content)

    def get_devices(
        self,
        device_names: List[str] = [],
        platform: Optional[str] = None,
        status: Optional[str] = None,
        udids: List[str] = [],
    ) -> SonicCloudResponse:
        api = GetDevicesApi(host=self.host, _session=self.session)
        data = GetDevicesRequest(
            devices_names=device_names,
            platform=platform,
            status=status,
            udIds=udids,
            uuidKey=self.uuid_key,
        ).dict(exclude_none=True)

        response = api.call(json=data)
        return SonicCloudResponse.parse_raw(b=response.content)

    def lock_device(self, device_udid: str) -> SonicCloudResponse:
        api = LockDeviceApi(host=self.host, _session=self.session)
        query_params = LockDeviceQueryParams(deviceUDID=device_udid, uuidKey=self.uuid_key).dict(exclude_none=True)

        response = api.call(params=query_params)
        return SonicCloudResponse.parse_raw(b=response.content)

    def release_device(self, device_udid: str) -> SonicCloudResponse:
        api = ReleaseDeviceApi(host=self.host, _session=self.session)
        query_params = ReleaseDeviceQueryParams(deviceUDID=device_udid, uuidKey=self.uuid_key).dict(exclude_none=True)

        response = api.call(params=query_params)
        return SonicCloudResponse.parse_raw(b=response.content)

    def get_available_appium_ports_by_device_udid(
        self,
        device_udid: Optional[str] = None,
        agent_id: Optional[Union[str, int]] = None,
        by_agent_id: bool = False,
    ) -> SonicCloudResponse:

        if by_agent_id:
            if not agent_id:
                raise ValueError("'agent_id' must be filled when 'by_agent_id' = True")
            else:
                agent_id = int(agent_id)
        else:
            if not device_udid:
                raise ValueError("'device_udid' must be filled when 'by_agent_id' = False")

        api = GetAvailableAppiumPortApi(host=self.host, _session=self.session)
        data = GetAvailableAppiumPortRequest(udid=device_udid, agentId=agent_id, byAgentId=by_agent_id).dict(
            exclude_none=True
        )

        response = api.call(json=data)
        return SonicCloudResponse.parse_raw(b=response.content)
