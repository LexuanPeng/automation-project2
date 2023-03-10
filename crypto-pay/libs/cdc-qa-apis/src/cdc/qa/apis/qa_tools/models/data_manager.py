from enum import Enum
from typing import List, Optional, Union

from pydantic import Field

from ..base_models import FrozenBaseModel, QAToolResponse, QAToolSignedRequest


class DataType(Enum):
    JSON = "J"
    STRING = "S"


# data_manager/v1/services/api_get_service_datas/
class ServiceDataDetail(FrozenBaseModel):
    id: int = Field(description="id")
    name: str = Field(description="name")
    description: Optional[str] = Field(description="description")
    data: str = Field(description="data")
    data_type: str = Field(description="data_type J for json")
    env: Optional[str] = Field(description="env")
    tags: Optional[List[str]] = Field(description="tags")
    is_lock: int = Field(description="is_lock 1 locked, 0 for unlocked")
    status: str = Field(description="status")


class GetServiceDatasData(FrozenBaseModel):
    page: int = Field(description="page")
    size: int = Field(description="size")
    total: int = Field(description="total")
    result: List[ServiceDataDetail]


class GetServiceDatasResponse(QAToolResponse):
    data: GetServiceDatasData


class GetServiceDatasRequestParams(FrozenBaseModel):
    service_id: int = Field(description="Service ID")
    name: Optional[str] = Field(description="name")
    is_lock: Optional[int] = Field(description="Default None")
    env: Optional[str] = Field(description="env filter")
    tags: Optional[List[str]] = Field(description="tags filter")
    size: Optional[int] = Field(description="Page size (Default: 10, Max: 200)")
    page: Optional[int] = Field(description="Page number 1")


class GetServiceDatasRequest(QAToolSignedRequest):
    method: str = "services/api_get_service_datas"
    params: GetServiceDatasRequestParams = Field()


# data_manager/v1/datas/api_lock/
class DataApiLockResponse(QAToolResponse):
    pass


class DataApiLockRequestParams(FrozenBaseModel):
    service_id: int = Field(description="Service ID")
    data_id: int = Field(description="data id")
    type: str = Field(description="lock type: lock/release")
    ttl: Optional[int] = Field(description="lock duration seconds, default:3600")


class DataApiLockRequest(QAToolSignedRequest):
    method: str = "datas/api_lock"
    params: DataApiLockRequestParams = Field()


# data_manager/v1/datas/api_create/
class CreateServiceDataResponse(QAToolResponse):
    pass


class CreateServiceDataRequestParams(FrozenBaseModel):
    service_id: int = Field(description="Service ID")
    name: str = Field(description="name")
    data_type: str = Field(description="Data Type")
    description: Optional[str] = Field(description="description")
    data: str = Field(description="Data")
    env: Optional[str] = Field(description="env")
    tags: Optional[List[str]] = Field(description="tags")


class CreateServiceDataRequest(QAToolSignedRequest):
    method: str = "datas/api_create"
    params: CreateServiceDataRequestParams = Field()


# data_manager/v1/datas/api_update/
class UpdateServiceDataResponse(QAToolResponse):
    pass


class UpdateServiceDataRequestParams(CreateServiceDataRequestParams, FrozenBaseModel):
    data_id: int = Field(description="Data ID")


class UpdateServiceDataRequest(QAToolSignedRequest):
    method: str = "datas/api_update"
    params: UpdateServiceDataRequestParams = Field()


# data_manager/v1/datas/api_delete/
class DeleteServiceDataResponse(QAToolResponse):
    pass


class DeleteServiceDataRequestParams(FrozenBaseModel):
    data_id: Union[int, List[int]] = Field(description="Data ID")
    service_id: int = Field(description="Service ID")


class DeleteServiceDataRequest(QAToolSignedRequest):
    method: str = "datas/api_delete"
    params: DeleteServiceDataRequestParams = Field()
