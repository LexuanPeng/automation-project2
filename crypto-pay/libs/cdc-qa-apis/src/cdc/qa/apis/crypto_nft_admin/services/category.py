from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.crypto_nft_admin.models import NFTRestApi, NFTRestService, category


class GetCategoryListApi(NFTRestApi):
    path = "/api/asset/category/list/"
    method = HttpMethods.GET
    request_params_type = category.GetCategoryListParams
    response_type = category.GetCategoryListResponse


class GetCategoryListAbnormalApi(NFTRestApi):
    path = "/api/asset/category/list/"
    method = HttpMethods.GET
    request_params_type = category.GetCategoryListParams
    response_type = category.GetCategoryListAbnormalResponse


class GetCategoryListShowStatusApi(NFTRestApi):
    path = "/api/asset/category/list/active/"
    method = HttpMethods.GET
    request_params_type = category.GetCategoryListShowStatusParams
    response_type = category.GetCategoryListShowStatusResponse


class GetCategoryListShowStatusAbnormalApi(NFTRestApi):
    path = "/api/asset/category/list/active/"
    method = HttpMethods.GET
    request_params_type = category.GetCategoryListShowStatusParams
    response_type = category.GetCategoryListShowStatusAbnormalResponse


class CreateCategoryApi(NFTRestApi):
    path = "/api/asset/category/"
    method = HttpMethods.POST
    request_params_type = category.CreateCategoryParams
    response_type = category.CreateCategoryResponse


class EditCategoryApi(NFTRestApi):
    def path(self, path_params: category.EditCategoryPathParams):
        return f"/api/asset/category/{path_params.id}"

    method = HttpMethods.PUT
    path_params_type = category.EditCategoryPathParams
    request_params_type = category.EditCategoryParams
    response_type = category.EditCategoryResponse


class CreateCategoryDWApi(NFTRestApi):
    path = "/api/asset/category/dw/"
    method = HttpMethods.POST
    request_params_type = category.CreateCategoryDWParams
    response_type = category.CreateCategoryDWResponse


class EditCategoryDWApi(NFTRestApi):
    def path(self, path_params: category.EditCategoryDWPathParams):
        return f"/api/asset/category/dw/{path_params.id}"

    method = HttpMethods.PUT
    request_params_type = category.EditCategoryDWParams
    response_type = category.EditCategoryDWResponse


class UpdateCategoryStatusApi(NFTRestApi):
    def path(self, path_params: category.UpdateCategoryStatusPathParams):
        return f"/api/asset/category/{path_params.id}/switch"

    method = HttpMethods.PUT
    request_params_type = category.UpdateCategoryStatusParams
    response_type = category.UpdateCategoryStatusResponse


class UpdateCategoryStatusDWApi(NFTRestApi):
    def path(self, path_params: category.UpdateCategoryStatusDWPathParams):
        return f"/api/asset/category/dw/{path_params.id}/switch"

    method = HttpMethods.PUT
    request_params_type = category.UpdateCategoryStatusDWParams
    response_type = category.UpdateCategoryStatusDWResponse


class CategoryService(NFTRestService):
    def query_category_list(
        self,
        current_page: int,
        page_size: int = None,
        name: str = None,
    ) -> category.GetCategoryListResponse:
        api = GetCategoryListApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = category.GetCategoryListParams(current_page=current_page, page_size=page_size, name=name)
        return category.GetCategoryListResponse.parse_raw(b=api.call(json=request.dict()).content)

    def query_category_list_abnormal(
        self,
        current_page: int,
        page_size: int = None,
        name: str = None,
    ) -> category.GetCategoryListAbnormalResponse:
        api = GetCategoryListAbnormalApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = category.GetCategoryListParams(current_page=current_page, page_size=page_size, name=name)
        return category.GetCategoryListAbnormalResponse.parse_raw(b=api.call(json=request.dict()).content)

    def query_category_list_show_status(
        self,
        current_page: int,
        page_size: int = None,
        name: str = None,
    ) -> category.GetCategoryListShowStatusResponse:
        api = GetCategoryListShowStatusApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = category.GetCategoryListShowStatusParams(current_page=current_page, page_size=page_size, name=name)
        return category.GetCategoryListShowStatusResponse.parse_raw(b=api.call(json=request.dict()).content)

    def query_category_list_show_status_abnormal(
        self,
        current_page: int,
        page_size: int = None,
        name: str = None,
    ) -> category.GetCategoryListShowStatusAbnormalResponse:
        api = GetCategoryListShowStatusAbnormalApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = category.GetCategoryListShowStatusParams(current_page=current_page, page_size=page_size, name=name)
        return category.GetCategoryListShowStatusAbnormalResponse.parse_raw(b=api.call(json=request.dict()).content)

    def create_category_normal(
        self,
        name: str,
    ) -> category.CreateCategoryResponse:
        api = CreateCategoryApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = category.CreateCategoryParams(name=name)
        b = api.call(json=request.dict())
        return b

    def create_category_abnormal(
        self,
        name: str,
    ) -> category.CreateCategoryResponse:
        api = CreateCategoryApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = category.CreateCategoryParams(name=name)
        return category.CreateCategoryResponse.parse_raw(b=api.call(json=request.dict()).content)

    def edit_category_normal(
        self,
        id: str,
        name: str,
    ) -> category.EditCategoryResponse:
        api = EditCategoryApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = category.EditCategoryPathParams(id=id)
        request = category.EditCategoryParams(name=name)
        b = api.call(path_params=path_params, json=request.dict())
        return b

    def edit_category_abnormal(
        self,
        id: str,
        name: str,
    ) -> category.EditCategoryResponse:
        api = EditCategoryApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = category.EditCategoryPathParams(id=id)
        request = category.EditCategoryParams(name=name)
        return category.EditCategoryResponse.parse_raw(b=api.call(path_params=path_params, json=request.dict()).content)

    def create_category_dw_normal(
        self,
        name: str,
    ) -> category.CreateCategoryDWResponse:
        api = CreateCategoryDWApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = category.CreateCategoryDWParams(name=name)
        b = api.call(json=request.dict())
        return b

    def create_category_dw_abnormal(
        self,
        name: str,
    ) -> category.CreateCategoryDWResponse:
        api = CreateCategoryDWApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = category.CreateCategoryDWParams(name=name)
        return category.CreateCategoryDWResponse.parse_raw(b=api.call(json=request.dict()).content)

    def edit_category_dw_normal(
        self,
        id: str,
        name: str,
    ) -> category.EditCategoryDWResponse:
        api = EditCategoryDWApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = category.EditCategoryDWPathParams(id=id)
        request = category.EditCategoryDWParams(name=name)
        b = api.call(path_params=path_params, json=request.dict())
        return b

    def edit_category_dw_abnormal(
        self,
        id: str,
        name: str,
    ) -> category.EditCategoryDWResponse:
        api = EditCategoryDWApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = category.EditCategoryDWPathParams(id=id)
        request = category.EditCategoryDWParams(name=name)
        return category.EditCategoryDWResponse.parse_raw(
            b=api.call(path_params=path_params, json=request.dict()).content
        )

    def update_category_status_normal(
        self,
        id: str,
        show: bool,
    ) -> category.UpdateCategoryStatusResponse:
        api = UpdateCategoryStatusApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = category.UpdateCategoryStatusPathParams(id=id)
        request = category.UpdateCategoryStatusParams(show=show)
        b = api.call(path_params=path_params, json=request.dict())
        return b

    def update_category_status_abnormal(
        self,
        id: str,
        show: bool,
    ) -> category.UpdateCategoryStatusResponse:
        api = UpdateCategoryStatusApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = category.UpdateCategoryStatusPathParams(id=id)
        request = category.UpdateCategoryStatusParams(show=show)
        return category.UpdateCategoryStatusResponse.parse_raw(
            b=api.call(path_params=path_params, json=request.dict()).content
        )

    def update_category_status_dw_normal(
        self,
        id: str,
        show: bool,
    ) -> category.UpdateCategoryStatusDWResponse:
        api = UpdateCategoryStatusDWApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = category.UpdateCategoryStatusDWPathParams(id=id)
        request = category.UpdateCategoryStatusDWParams(show=show)
        b = api.call(path_params=path_params, json=request.dict())
        return b

    def update_category_status_dw_abnormal(
        self,
        id: str,
        show: bool,
    ) -> category.UpdateCategoryStatusDWResponse:
        api = UpdateCategoryStatusDWApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = category.UpdateCategoryStatusDWPathParams(id=id)
        request = category.UpdateCategoryStatusDWParams(show=show)
        return category.UpdateCategoryStatusDWResponse.parse_raw(
            b=api.call(path_params=path_params, json=request.dict()).content
        )
