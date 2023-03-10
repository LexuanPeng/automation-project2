from pathlib import Path
from typing import Union

from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.jumio.models import JumioRestApi, JumioRestService
from cdc.qa.apis.jumio.models.file import FileUploadRequestPathParams, FileUploadRequestQueryParams


class FileUploadApi(JumioRestApi):
    """Upload file to Jumio"""

    def path(self, path_params: FileUploadRequestPathParams):
        return path_params.upload_url_path

    method = HttpMethods.PUT
    headers = {"Content-Type": "application/octet-stream"}
    path_params_type = FileUploadRequestPathParams
    request_params_type = FileUploadRequestQueryParams
    response_type = int


class FileService(JumioRestService):
    def upload(self, upload_url_path: str, query_params: dict, file_path: Union[Path, str]) -> int:
        api = FileUploadApi(host=self.host, _session=self.session)
        path_params = FileUploadRequestPathParams(upload_url_path=upload_url_path)
        query_params = FileUploadRequestQueryParams(**query_params).dict(exclude_none=True, by_alias=True)
        data = open(file_path, "rb")

        response = api.call(path_params=path_params, params=query_params, data=data)
        return response.status_code
