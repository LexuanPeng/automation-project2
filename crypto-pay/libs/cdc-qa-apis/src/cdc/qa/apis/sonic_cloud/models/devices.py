from typing import Optional, List

from pydantic import Field

from cdc.qa.apis.sonic_cloud.models import FrozenBaseModel


class GetDevice(FrozenBaseModel):
    id: int


class GetAllDevicesRequest(FrozenBaseModel):
    pass


class GetDevicesRequest(FrozenBaseModel):
    deviceNames: Optional[List[str]] = Field()
    platform: Optional[str] = Field()
    status: Optional[str] = Field()
    udids: Optional[List[str]] = Field()
    uuidKey: str = Field()
