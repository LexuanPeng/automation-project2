from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.crypto_nft_admin.models import NFTRestApi, NFTRestService, dropaccess


class GetDropAccessApi(NFTRestApi):
    def path(self, path_params: dropaccess.GetDropAccessPathParams):
        return f"/api/asset/drop-access/{path_params.drop_id}"

    method = HttpMethods.GET
    path_params_type = dropaccess.GetDropAccessPathParams
    response_type = dropaccess.GetDropAccessResponse


class GetDropAccessAbnormalApi(NFTRestApi):
    def path(self, path_params: dropaccess.GetDropAccessPathParams):
        return f"/api/asset/drop-access/{path_params.drop_id}"

    method = HttpMethods.GET
    path_params_type = dropaccess.GetDropAccessPathParams
    response_type = dropaccess.GetDropAccessAbnormalResponse


class GrantItemToDropAccessApi(NFTRestApi):
    def path(self, path_params: dropaccess.GrantItemToDropAccessPathParams):
        return f"/api/asset/drop-access/{path_params.drop_id}/grant/"

    method = HttpMethods.POST
    path_params_type = dropaccess.GrantItemToDropAccessPathParams
    request_params_type = dropaccess.GrantItemToDropAccessDetailParams
    response_type = dropaccess.GrantItemToDropAccessResponse


class CreateDropAccessApi(NFTRestApi):
    path = "/api/asset/drop-access/"
    method = HttpMethods.POST
    request_params_type = dropaccess.CreateDropAccessDetailParams
    response_type = dropaccess.CreateDropAccessResponse


class EditDropAccessApi(NFTRestApi):
    def path(self, path_params: dropaccess.EditDropAccessPathParams):
        return f"/api/asset/drop-access/{path_params.drop_id}/config/"

    method = HttpMethods.PUT
    path_params_type = dropaccess.EditDropAccessPathParams
    request_params_type = dropaccess.EditDropAccessDetailParams
    response_type = dropaccess.EditDropAccessResponse


class UpdateDropAccessReservedCountApi(NFTRestApi):
    def path(self, path_params: dropaccess.UpdateDropAccessReservedCountPathParams):
        return f"api/asset/drop-access/{path_params.drop_id}/{path_params.drop_item_id}/"

    method = HttpMethods.PUT
    path_params_type = dropaccess.UpdateDropAccessReservedCountPathParams
    request_params_type = dropaccess.UpdateDropAccessReservedCountDetailParams
    response_type = dropaccess.UpdateDropAccessReservedCountResponse


class DeleteConfiguredDropAccessApi(NFTRestApi):
    def path(self, path_params: dropaccess.DeleteConfiguredDropAccessPathParams):
        return f"/api/asset/drop-access/{path_params.drop_id}/"

    method = HttpMethods.DELETE
    path_params_type = dropaccess.DeleteConfiguredDropAccessPathParams
    response_type = dropaccess.DeleteConfiguredDropAccessResponse


class DeleteGrantedDropAccessItemApi(NFTRestApi):
    def path(self, path_params: dropaccess.DeleteGrantedDropAccessItemPathParams):
        return f"/api/asset/drop-access/{path_params.drop_id}/item/{path_params.item_id}/"

    method = HttpMethods.DELETE
    path_params_type = dropaccess.DeleteGrantedDropAccessItemPathParams
    response_type = dropaccess.DeleteGrantedDropAccessItemResponse


class CreateDropAccessDwApi(NFTRestApi):
    path = "/api/asset/drop-access/dw/"
    method = HttpMethods.POST
    request_params_type = dropaccess.CreateDropAccessDwDetailParams
    response_type = dropaccess.CreateDropAccessDwResponse


class EditDropAccessDwApi(NFTRestApi):
    def path(self, path_params: dropaccess.EditDropAccessDwPathParams):
        return f"/api/asset/drop-access/dw/{path_params.drop_id}/config/"

    method = HttpMethods.PUT
    path_params_type = dropaccess.EditDropAccessDwPathParams
    request_params_type = dropaccess.EditDropAccessDwDetailParams
    response_type = dropaccess.EditDropAccessDwResponse


class UpdateDropAccessReservedCountDwApi(NFTRestApi):
    def path(self, path_params: dropaccess.UpdateDropAccessReservedCountDwPathParams):
        return f"api/asset/drop-access/{path_params.drop_id}/{path_params.drop_item_id}/dw/"

    method = HttpMethods.PUT
    path_params_type = dropaccess.UpdateDropAccessReservedCountDwPathParams
    request_params_type = dropaccess.UpdateDropAccessReservedCountDwDetailParams
    response_type = dropaccess.UpdateDropAccessReservedCountDwResponse


class DeleteConfiguredDropAccessDwApi(NFTRestApi):
    def path(self, path_params: dropaccess.DeleteConfiguredDropAccessDwPathParams):
        return f"/api/asset/drop-access/{path_params.drop_id}/dw/"

    method = HttpMethods.DELETE
    path_params_type = dropaccess.DeleteConfiguredDropAccessDwPathParams
    response_type = dropaccess.DeleteConfiguredDropAccessDwResponse


class DeleteGrantedDropAccessItemDwApi(NFTRestApi):
    def path(self, path_params: dropaccess.DeleteGrantedDropAccessItemDwPathParams):
        return f"/api/asset/drop-access/{path_params.drop_id}/item/{path_params.item_id}/dw/"

    method = HttpMethods.DELETE
    path_params_type = dropaccess.DeleteGrantedDropAccessItemDwPathParams
    response_type = dropaccess.DeleteGrantedDropAccessItemDwResponse


class DropAccessService(NFTRestService):
    def get_dropaccess(
        self,
        drop_id: str,
    ) -> dropaccess.GetDropAccessResponse:
        api = GetDropAccessApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = dropaccess.GetDropAccessPathParams(drop_id=drop_id)
        return dropaccess.GetDropAccessResponse.parse_raw(b=api.call(path_params=path_params).content)

    def get_dropaccess_abnormal(
        self,
        drop_id: str,
    ) -> dropaccess.GetDropAccessAbnormalResponse:
        api = GetDropAccessAbnormalApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = dropaccess.GetDropAccessPathParams(drop_id=drop_id)
        return dropaccess.GetDropAccessAbnormalResponse.parse_raw(b=api.call(path_params=path_params).content)

    def grant_item_to_dropaccess(
        self,
        drop_id: str,
        item_list: list,
    ) -> dropaccess.GrantItemToDropAccessResponse:
        api = GrantItemToDropAccessApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = dropaccess.GrantItemToDropAccessPathParams(drop_id=drop_id)
        request = dropaccess.GrantItemToDropAccessDetailParams(item_list=item_list)
        b = api.call(
            path_params=path_params,
            json=request.dict(),
        )
        return b

    def grant_item_to_dropaccess_abnormal(
        self,
        drop_id: str,
        item_list: list,
    ) -> dropaccess.GrantItemToDropAccessResponse:
        api = GrantItemToDropAccessApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = dropaccess.GrantItemToDropAccessPathParams(drop_id=drop_id)
        request = dropaccess.GrantItemToDropAccessDetailParams(item_list=item_list)
        return dropaccess.GrantItemToDropAccessResponse.parse_raw(
            b=api.call(json=request.dict(), path_params=path_params).content
        )

    def create_dropaccess_dw_normal(
        self,
        description: str,
        title: str,
        drop_id: str,
        type: int,
        start_time: str = None,
        end_time: str = None,
    ) -> dropaccess.CreateDropAccessDwResponse:
        api = CreateDropAccessDwApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = dropaccess.CreateDropAccessDwDetailParams(
            description=description,
            title=title,
            drop_id=drop_id,
            type=type,
            start_time=start_time,
            end_time=end_time,
        )
        b = api.call(json=request.dict())
        return b

    def create_dropaccess_dw_abnormal(
        self,
        description: str,
        title: str,
        drop_id: str,
        type: int,
        start_time: str = None,
        end_time: str = None,
    ) -> dropaccess.CreateDropAccessDwResponse:
        api = CreateDropAccessDwApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = dropaccess.CreateDropAccessDwDetailParams(
            description=description,
            title=title,
            drop_id=drop_id,
            type=type,
            start_time=start_time,
            end_time=end_time,
        )
        return dropaccess.CreateDropAccessDwResponse.parse_raw(b=api.call(json=request.dict()).content)

    def edit_dropaccess_dw_normal(
        self,
        description: str,
        title: str,
        drop_id: str,
        type: int,
        start_time: str = None,
        end_time: str = None,
    ) -> dropaccess.EditDropAccessDwResponse:
        api = EditDropAccessDwApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = dropaccess.EditDropAccessDwPathParams(drop_id=drop_id)
        request = dropaccess.EditDropAccessDwDetailParams(
            description=description,
            title=title,
            type=type,
            start_time=start_time,
            end_time=end_time,
        )
        b = api.call(
            path_params=path_params,
            json=request.dict(),
        )
        return b

    def edit_dropaccess_dw_abnormal(
        self,
        description: str,
        title: str,
        drop_id: str,
        type: int,
        start_time: str = None,
        end_time: str = None,
    ) -> dropaccess.EditDropAccessDwResponse:
        api = EditDropAccessDwApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = dropaccess.EditDropAccessDwPathParams(drop_id=drop_id)
        request = dropaccess.EditDropAccessDwDetailParams(
            description=description,
            title=title,
            type=type,
            start_time=start_time,
            end_time=end_time,
        )
        return dropaccess.EditDropAccessDwResponse.parse_raw(
            b=api.call(
                path_params=path_params,
                json=request.dict(),
            ).content
        )

    def update_dropaccess_reserved_count_dw_normal(
        self,
        drop_id: str,
        drop_item_id: str,
        type: int,
        reserved_count: int,
    ) -> dropaccess.UpdateDropAccessReservedCountDwResponse:
        api = UpdateDropAccessReservedCountDwApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = dropaccess.UpdateDropAccessReservedCountDwPathParams(drop_id=drop_id, drop_item_id=drop_item_id)
        request = dropaccess.UpdateDropAccessReservedCountDwDetailParams(
            type=type,
            reserved_count=reserved_count,
        )
        b = api.call(
            path_params=path_params,
            json=request.dict(),
        )
        return b

    def update_dropaccess_reserved_count_dw_abnormal(
        self,
        drop_id: str,
        drop_item_id: str,
        type: int,
        reserved_count: int,
    ) -> dropaccess.UpdateDropAccessReservedCountDwResponse:
        api = UpdateDropAccessReservedCountDwApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = dropaccess.UpdateDropAccessReservedCountDwPathParams(drop_id=drop_id, drop_item_id=drop_item_id)
        request = dropaccess.UpdateDropAccessReservedCountDwDetailParams(
            type=type,
            reserved_count=reserved_count,
        )
        return dropaccess.UpdateDropAccessReservedCountDwResponse.parse_raw(
            b=api.call(
                path_params=path_params,
                json=request.dict(),
            ).content
        )

    def delete_configured_dropaccess_dw(
        self,
        drop_id: str,
    ) -> dropaccess.DeleteConfiguredDropAccessDwResponse:
        api = DeleteConfiguredDropAccessDwApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = dropaccess.DeleteConfiguredDropAccessDwPathParams(drop_id=drop_id)
        b = api.call(path_params=path_params)
        return b

    def delete_configured_dropaccess_dw_abnormal(
        self,
        drop_id: str,
    ) -> dropaccess.DeleteConfiguredDropAccessDwResponse:
        api = DeleteConfiguredDropAccessDwApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = dropaccess.DeleteConfiguredDropAccessDwPathParams(drop_id=drop_id)
        return dropaccess.DeleteConfiguredDropAccessDwResponse.parse_raw(b=api.call(path_params=path_params).content)

    def delete_granted_dropaccess_item_dw(
        self,
        drop_id: str,
        item_id: str,
    ) -> dropaccess.DeleteGrantedDropAccessItemDwResponse:
        api = DeleteGrantedDropAccessItemDwApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = dropaccess.DeleteGrantedDropAccessItemDwPathParams(drop_id=drop_id, item_id=item_id)
        b = api.call(path_params=path_params)
        return b

    def delete_granted_dropaccess_item_dw_abnormal(
        self,
        drop_id: str,
        item_id: str,
    ) -> dropaccess.DeleteGrantedDropAccessItemDwResponse:
        api = DeleteGrantedDropAccessItemDwApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = dropaccess.DeleteGrantedDropAccessItemDwPathParams(drop_id=drop_id, item_id=item_id)
        return dropaccess.DeleteGrantedDropAccessItemDwResponse.parse_raw(b=api.call(path_params=path_params).content)

    def create_dropaccess_normal(
        self,
        description: str,
        title: str,
        drop_id: str,
        type: int,
        start_time: str = None,
        end_time: str = None,
    ) -> dropaccess.CreateDropAccessResponse:
        api = CreateDropAccessApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = dropaccess.CreateDropAccessDetailParams(
            description=description,
            title=title,
            drop_id=drop_id,
            type=type,
            start_time=start_time,
            end_time=end_time,
        )
        b = api.call(json=request.dict())
        return b

    def create_dropaccess_abnormal(
        self,
        description: str,
        title: str,
        drop_id: str,
        type: int,
        start_time: str = None,
        end_time: str = None,
    ) -> dropaccess.CreateDropAccessResponse:
        api = CreateDropAccessApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = dropaccess.CreateDropAccessDetailParams(
            description=description,
            title=title,
            drop_id=drop_id,
            type=type,
            start_time=start_time,
            end_time=end_time,
        )
        return dropaccess.CreateDropAccessResponse.parse_raw(b=api.call(json=request.dict()).content)

    def edit_dropaccess_normal(
        self,
        description: str,
        title: str,
        drop_id: str,
        type: int,
        start_time: str = None,
        end_time: str = None,
    ) -> dropaccess.EditDropAccessResponse:
        api = EditDropAccessApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = dropaccess.EditDropAccessPathParams(drop_id=drop_id)
        request = dropaccess.EditDropAccessDetailParams(
            description=description,
            title=title,
            type=type,
            start_time=start_time,
            end_time=end_time,
        )
        b = api.call(
            path_params=path_params,
            json=request.dict(),
        )
        return b

    def edit_dropaccess_abnormal(
        self,
        description: str,
        title: str,
        drop_id: str,
        type: int,
        start_time: str = None,
        end_time: str = None,
    ) -> dropaccess.EditDropAccessResponse:
        api = EditDropAccessApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = dropaccess.EditDropAccessPathParams(drop_id=drop_id)
        request = dropaccess.EditDropAccessDetailParams(
            description=description,
            title=title,
            type=type,
            start_time=start_time,
            end_time=end_time,
        )
        return dropaccess.EditDropAccessResponse.parse_raw(
            b=api.call(
                path_params=path_params,
                json=request.dict(),
            ).content
        )

    def update_dropaccess_reserved_count_normal(
        self,
        drop_id: str,
        drop_item_id: str,
        type: int,
        reserved_count: int,
    ) -> dropaccess.UpdateDropAccessReservedCountResponse:
        api = UpdateDropAccessReservedCountApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = dropaccess.UpdateDropAccessReservedCountPathParams(drop_id=drop_id, drop_item_id=drop_item_id)
        request = dropaccess.UpdateDropAccessReservedCountDetailParams(
            type=type,
            reserved_count=reserved_count,
        )
        b = api.call(
            path_params=path_params,
            json=request.dict(),
        )
        return b

    def update_dropaccess_reserved_count_abnormal(
        self,
        drop_id: str,
        drop_item_id: str,
        type: int,
        reserved_count: int,
    ) -> dropaccess.UpdateDropAccessReservedCountResponse:
        api = UpdateDropAccessReservedCountApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = dropaccess.UpdateDropAccessReservedCountPathParams(drop_id=drop_id, drop_item_id=drop_item_id)
        request = dropaccess.UpdateDropAccessReservedCountDetailParams(
            type=type,
            reserved_count=reserved_count,
        )
        return dropaccess.UpdateDropAccessReservedCountResponse.parse_raw(
            b=api.call(
                path_params=path_params,
                json=request.dict(),
            ).content
        )

    def delete_configured_dropaccess(
        self,
        drop_id: str,
    ) -> dropaccess.DeleteConfiguredDropAccessResponse:
        api = DeleteConfiguredDropAccessApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = dropaccess.DeleteConfiguredDropAccessPathParams(drop_id=drop_id)
        b = api.call(path_params=path_params)
        return b

    def delete_configured_dropaccess_abnormal(
        self,
        drop_id: str,
    ) -> dropaccess.DeleteConfiguredDropAccessResponse:
        api = DeleteConfiguredDropAccessApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = dropaccess.DeleteConfiguredDropAccessPathParams(drop_id=drop_id)
        return dropaccess.DeleteConfiguredDropAccessResponse.parse_raw(b=api.call(path_params=path_params).content)

    def delete_granted_dropaccess_item(
        self,
        drop_id: str,
        item_id: str,
    ) -> dropaccess.DeleteGrantedDropAccessItemResponse:
        api = DeleteGrantedDropAccessItemApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = dropaccess.DeleteGrantedDropAccessItemPathParams(drop_id=drop_id, item_id=item_id)
        b = api.call(path_params=path_params)
        return b

    def delete_granted_dropaccess_item_abnormal(
        self,
        drop_id: str,
        item_id: str,
    ) -> dropaccess.DeleteGrantedDropAccessItemResponse:
        api = DeleteGrantedDropAccessItemApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = dropaccess.DeleteGrantedDropAccessItemPathParams(drop_id=drop_id, item_id=item_id)
        return dropaccess.DeleteGrantedDropAccessItemResponse.parse_raw(b=api.call(path_params=path_params).content)
