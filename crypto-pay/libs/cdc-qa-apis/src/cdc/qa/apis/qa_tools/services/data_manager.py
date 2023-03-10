import json
from typing import List, Union

from cdc.qa.apis.common.models.rest_api import HttpMethods

from ..models.data_manager import (
    DataApiLockRequest,
    DataApiLockRequestParams,
    DataApiLockResponse,
    GetServiceDatasRequest,
    GetServiceDatasRequestParams,
    GetServiceDatasResponse,
    CreateServiceDataRequest,
    CreateServiceDataResponse,
    DataType,
    CreateServiceDataRequestParams,
    UpdateServiceDataResponse,
    UpdateServiceDataRequest,
    UpdateServiceDataRequestParams,
    DeleteServiceDataResponse,
    DeleteServiceDataRequest,
    DeleteServiceDataRequestParams,
)
from . import QAToolRestApi, QAToolRestService


class GetServiceDatasApi(QAToolRestApi):
    path = "data_manager/v1/services/api_get_service_datas/"
    method = HttpMethods.POST
    request_data_type = GetServiceDatasRequest
    response_type = GetServiceDatasResponse


class DataApiLockApi(QAToolRestApi):
    path = "data_manager/v1/datas/api_lock/"
    method = HttpMethods.POST
    request_data_type = DataApiLockRequest
    response_type = DataApiLockResponse


class CreateServiceDataApi(QAToolRestApi):
    path = "data_manager/v1/datas/api_create/"
    method = HttpMethods.POST
    request_data_type = CreateServiceDataRequest
    response_type = CreateServiceDataResponse


class UpdateServiceDataApi(QAToolRestApi):
    path = "data_manager/v1/datas/api_update/"
    method = HttpMethods.POST
    request_data_type = UpdateServiceDataRequest
    response_type = UpdateServiceDataResponse


class DeleteServiceDataApi(QAToolRestApi):
    path = "data_manager/v1/datas/api_delete/"
    method = HttpMethods.POST
    request_data_type = DeleteServiceDataRequest
    response_type = DeleteServiceDataResponse


class DataManagerService(QAToolRestService):
    def get_service_datas(
        self,
        service_id: int,
        name: str = None,
        env: str = None,
        tags: List[str] = None,
        is_lock: Union[int, None] = 0,
        size: int = 10,
        page: int = 1,
    ) -> GetServiceDatasResponse:
        api = GetServiceDatasApi(host=self.host, _session=self.session)
        payload = GetServiceDatasRequest(
            params=GetServiceDatasRequestParams(
                service_id=service_id, name=name, env=env, tags=tags, is_lock=is_lock, size=size, page=page
            ),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)

        response = api.call(data=payload)
        return GetServiceDatasResponse.parse_raw(b=response.content)

    def lock_data(self, service_id: int, data_id: int, ttl: int = 3600) -> DataApiLockResponse:
        api = DataApiLockApi(host=self.host, _session=self.session)
        payload = DataApiLockRequest(
            params=DataApiLockRequestParams(
                service_id=service_id,
                data_id=data_id,
                type="lock",
                ttl=ttl,
            ),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)

        response = api.call(data=payload)
        return DataApiLockResponse.parse_raw(b=response.content)

    def release_data(self, service_id: int, data_id: int) -> DataApiLockResponse:
        api = DataApiLockApi(host=self.host, _session=self.session)
        payload = DataApiLockRequest(
            params=DataApiLockRequestParams(
                service_id=service_id,
                data_id=data_id,
                type="release",
            ),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)

        response = api.call(data=payload)
        return DataApiLockResponse.parse_raw(b=response.content)

    def create_data(
        self,
        service_id: int,
        name: str,
        data_type: DataType,
        description: str = None,
        data: Union[str, dict] = "",
        env: str = None,
        tags: List[str] = None,
    ) -> CreateServiceDataResponse:
        api = CreateServiceDataApi(host=self.host, _session=self.session)
        if data_type == DataType.JSON and data == "":
            data = {}
        if isinstance(data, dict):
            data = json.dumps(data)
        payload = CreateServiceDataRequest(
            params=CreateServiceDataRequestParams(
                service_id=service_id,
                name=name,
                data_type=data_type.value,
                description=description,
                data=data,
                env=env,
                tags=tags,
            ),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)

        response = api.call(data=payload)
        return CreateServiceDataResponse.parse_raw(b=response.content)

    def update_data(
        self,
        data_id: int,
        service_id: int,
        name: str,
        data_type: DataType,
        description: str = None,
        data: Union[str, dict] = "",
        env: str = None,
        tags: List[str] = None,
    ) -> UpdateServiceDataResponse:
        api = UpdateServiceDataApi(host=self.host, _session=self.session)
        if data_type == DataType.JSON and data == "":
            data = {}
        if isinstance(data, dict):
            data = json.dumps(data)

        payload = UpdateServiceDataRequest(
            params=UpdateServiceDataRequestParams(
                data_id=data_id,
                service_id=service_id,
                name=name,
                data_type=data_type.value,
                description=description,
                data=data,
                env=env,
                tags=tags,
            ),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)

        response = api.call(data=payload)
        return UpdateServiceDataResponse.parse_raw(b=response.content)

    def delete_data(
        self,
        data_id: Union[int, List[int]],
        service_id: int,
    ) -> DeleteServiceDataResponse:
        api = DeleteServiceDataApi(host=self.host, _session=self.session)
        payload = DeleteServiceDataRequest(
            params=DeleteServiceDataRequestParams(
                data_id=data_id,
                service_id=service_id,
            ),
            api_key=self.api_key,
            secret_key=self.secret_key,
        ).json(exclude_none=True)

        response = api.call(data=payload)
        return DeleteServiceDataResponse.parse_raw(b=response.content)
