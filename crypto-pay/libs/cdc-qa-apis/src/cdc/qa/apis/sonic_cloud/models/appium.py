from typing import Optional, List

from pydantic import Field

from cdc.qa.apis.sonic_cloud.models import FrozenBaseModel


class CloseAppiumSessionQueryParams(FrozenBaseModel):
    deviceUDID: Optional[str] = Field()
    sessionId: Optional[str] = Field()


class CreateAppiumSessionQueryParams(FrozenBaseModel):
    deviceUDID: Optional[str] = Field()
    sessionId: Optional[str] = Field()
    appiumPort: Optional[str] = Field()
    wdaLocalPort: Optional[str] = Field()
    mjpegServerPort: Optional[str] = Field()


class EndAppiumSessionRequest(FrozenBaseModel):
    id: Optional[str] = Field()


class GetAllDevicesRequest(FrozenBaseModel):
    pass


class GetDevicesRequest(FrozenBaseModel):
    deviceNames: Optional[List[str]] = Field()
    platform: Optional[str] = Field()
    status: Optional[str] = Field()
    udIds: Optional[List[str]] = Field()
    uuidKey: str = Field()


class LockDeviceQueryParams(FrozenBaseModel):
    deviceUDID: str = Field()
    uuidKey: str = Field()


class ReleaseDeviceQueryParams(FrozenBaseModel):
    deviceUDID: str = Field()
    uuidKey: str = Field()


class GetAvailableAppiumPortRequest(FrozenBaseModel):
    udid: Optional[str] = Field()
    agentId: Optional[str] = Field()
    byAgentId: bool = Field()
