from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.crypto_nft_admin.models import NFTRestApi, NFTRestService, pack


class GetPackApi(NFTRestApi):
    path = "/api/asset/pack/list/"
    method = HttpMethods.POST
    request_params_type = pack.GetPackDetailParams
    response_type = pack.GetPackResponse


class GetPackAbnormalApi(NFTRestApi):
    path = "/api/asset/pack/list/"
    method = HttpMethods.POST
    request_params_type = pack.GetPackDetailParams
    response_type = pack.GetPackAbnormalResponse


class GetPackByUuidApi(NFTRestApi):
    def path(self, path_params: pack.GetPackByUuidPathParams):
        return f"/api/asset/pack/{path_params.uuid}"

    method = HttpMethods.GET
    path_params_type = pack.GetPackByUuidPathParams
    response_type = pack.GetPackByUuidResponse


class GetPackByUuidAbnormalApi(NFTRestApi):
    def path(self, path_params: pack.GetPackByUuidPathParams):
        return f"/api/asset/pack/{path_params.uuid}"

    method = HttpMethods.GET
    path_params_type = pack.GetPackByUuidPathParams
    response_type = pack.GetPackByUuidAbnormalResponse


class CreatePackApi(NFTRestApi):
    path = "/api/asset/pack/"
    method = HttpMethods.POST
    request_params_type = pack.CreatePackDetailParams
    response_type = pack.CreatePackResponse


class EditPackApi(NFTRestApi):
    def path(self, path_params: pack.EditPackPathParams):
        return f"/api/asset/pack/{path_params.uuid}"

    method = HttpMethods.PUT
    path_params_type = pack.EditPackPathParams
    request_params_type = pack.EditPackDetailParams
    response_type = pack.EditPackResponse


class CreatePackDWApi(NFTRestApi):
    path = "/api/asset/pack/createDW/"
    method = HttpMethods.POST
    request_params_type = pack.CreatePackDWDetailParams
    response_type = pack.CreatePackDWResponse


class EditPackDWApi(NFTRestApi):
    def path(self, path_params: pack.EditPackDWPathParams):
        return f"/api/asset/pack/editDW/{path_params.uuid}"

    method = HttpMethods.PUT
    request_params_type = pack.EditPackDWDetailParams
    response_type = pack.EditPackDWResponse


class CreatePackItemsApi(NFTRestApi):
    def path(self, path_params: pack.CreatePackItemsPathParams):
        return f"/api/asset/pack-item/pack/{path_params.pack_id}/item"

    method = HttpMethods.POST
    request_params_type = pack.CreatePackItemsDetailParams
    response_type = pack.CreatePackItemsResponse


class EditPackItemsApi(NFTRestApi):
    def path(self, path_params: pack.EditPackItemsPathParams):
        return f"/api/asset/pack-item/pack/{path_params.pack_id}/item"

    method = HttpMethods.PUT
    request_params_type = pack.EditPackItemsDetailParams
    response_type = pack.EditPackItemsResponse


class PackService(NFTRestService):
    def query_pack(
        self,
        current_page: int,
        page_size: int = None,
        id: str = None,
        name: str = None,
        creator_uuids: list = [],
    ) -> pack.GetPackResponse:
        api = GetPackApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = pack.GetPackDetailParams(
            current_page=current_page, page_size=page_size, id=id, name=name, creator_uuids=creator_uuids
        )
        return pack.GetPackResponse.parse_raw(b=api.call(json=request.dict()).content)

    def query_pack_abnormal(
        self,
        current_page: int,
        page_size: int = None,
        id: str = None,
        name: str = None,
        creator_uuids: list = [],
    ) -> pack.GetPackAbnormalResponse:
        api = GetPackAbnormalApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = pack.GetPackDetailParams(
            current_page=current_page, page_size=page_size, id=id, name=name, creator_uuids=creator_uuids
        )
        return pack.GetPackAbnormalResponse.parse_raw(b=api.call(json=request.dict()).content)

    def query_pack_by_uuid(
        self,
        uuid: str,
    ) -> pack.GetPackByUuidResponse:
        api = GetPackByUuidApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = pack.GetPackByUuidPathParams(uuid=uuid)
        return pack.GetPackByUuidResponse.parse_raw(b=api.call(path_params=path_params).content)

    def query_pack_by_uuid_abnormal(
        self,
        uuid: str,
    ) -> pack.GetPackByUuidAbnormalResponse:
        api = GetPackByUuidAbnormalApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = pack.GetPackByUuidPathParams(uuid=uuid)
        return pack.GetPackByUuidAbnormalResponse.parse_raw(b=api.call(path_params=path_params).content)

    def create_pack_normal(
        self,
        name: str,
        cover: str,
        description: str,
        creator_id: str,
        collectibles: int,
        quantity: int,
        asset_ids: list = [],
        collection_id: str = None,
    ) -> pack.CreatePackResponse:
        api = CreatePackApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = pack.CreatePackDetailParams(
            name=name,
            description=description,
            creator_id=creator_id,
            collectibles=collectibles,
            asset_ids=asset_ids,
            cover=cover,
            quantity=quantity,
            collection_id=collection_id,
        )
        b = api.call(json=request.dict())
        return b

    def create_pack_abnormal(
        self,
        name: str,
        cover: str,
        description: str,
        creator_id: str,
        collectibles: int,
        quantity: int,
        asset_ids: list = [],
        collection_id: str = None,
    ) -> pack.CreatePackResponse:
        api = CreatePackApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = pack.CreatePackDetailParams(
            name=name,
            description=description,
            creator_id=creator_id,
            collectibles=collectibles,
            asset_ids=asset_ids,
            cover=cover,
            quantity=quantity,
            collection_id=collection_id,
        )
        return pack.CreatePackResponse.parse_raw(b=api.call(json=request.dict()).content)

    def edit_pack_normal(
        self,
        uuid: str,
        name: str,
        cover: str,
        description: str,
        collectibles: int,
        blocked: bool,
        max_per_order: int,
        asset_ids: list = [],
        collection_id: str = None,
        max_per_user: int = None,
        remark: str = None,
    ) -> pack.EditPackResponse:
        api = EditPackApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = pack.EditPackPathParams(uuid=uuid)
        request = pack.EditPackDetailParams(
            name=name,
            description=description,
            collectibles=collectibles,
            asset_ids=asset_ids,
            cover=cover,
            collection_id=collection_id,
            blocked=blocked,
            max_per_user=max_per_user,
            max_per_order=max_per_order,
            remark=remark,
        )
        b = api.call(path_params=path_params, json=request.dict())
        return b

    def edit_pack_abnormal(
        self,
        uuid: str,
        name: str,
        cover: str,
        description: str,
        collectibles: int,
        blocked: bool,
        max_per_order: int,
        asset_ids: list = [],
        collection_id: str = None,
        max_per_user: int = None,
        remark: str = None,
    ) -> pack.EditPackResponse:
        api = EditPackApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = pack.EditPackPathParams(uuid=uuid)
        request = pack.EditPackDetailParams(
            name=name,
            description=description,
            collectibles=collectibles,
            asset_ids=asset_ids,
            cover=cover,
            collection_id=collection_id,
            blocked=blocked,
            max_per_user=max_per_user,
            max_per_order=max_per_order,
            remark=remark,
        )
        return pack.EditPackResponse.parse_raw(b=api.call(path_params=path_params, json=request.dict()).content)

    def create_pack_double_write_normal(
        self,
        name: str,
        cover: str,
        description: str,
        creator_id: str,
        collectibles: int,
        quantity: int,
        asset_ids: list = [],
        collection_id: str = None,
    ) -> pack.CreatePackDWResponse:
        api = CreatePackDWApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = pack.CreatePackDWDetailParams(
            name=name,
            description=description,
            creator_id=creator_id,
            collectibles=collectibles,
            asset_ids=asset_ids,
            cover=cover,
            quantity=quantity,
            collection_id=collection_id,
        )
        b = api.call(json=request.dict())
        return b

    def create_pack_double_write_abnormal(
        self,
        name: str,
        cover: str,
        description: str,
        creator_id: str,
        collectibles: int,
        quantity: int,
        asset_ids: list = [],
        collection_id: str = None,
    ) -> pack.CreatePackDWResponse:
        api = CreatePackDWApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = pack.CreatePackDWDetailParams(
            name=name,
            description=description,
            creator_id=creator_id,
            collectibles=collectibles,
            asset_ids=asset_ids,
            cover=cover,
            quantity=quantity,
            collection_id=collection_id,
        )
        return pack.CreatePackDWResponse.parse_raw(b=api.call(json=request.dict()).content)

    def edit_pack_double_write_normal(
        self,
        uuid: str,
        name: str,
        cover: str,
        description: str,
        collectibles: int,
        blocked: bool,
        max_per_order: int,
        asset_ids: list = [],
        collection_id: str = None,
        max_per_user: int = None,
        remark: str = None,
    ) -> pack.EditPackDWResponse:
        api = EditPackDWApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = pack.EditPackDWPathParams(uuid=uuid)
        request = pack.EditPackDWDetailParams(
            name=name,
            description=description,
            collectibles=collectibles,
            asset_ids=asset_ids,
            cover=cover,
            collection_id=collection_id,
            blocked=blocked,
            max_per_user=max_per_user,
            max_per_order=max_per_order,
            remark=remark,
        )
        b = api.call(path_params=path_params, json=request.dict())
        return b

    def edit_pack_double_write_abnormal(
        self,
        uuid: str,
        name: str,
        cover: str,
        description: str,
        collectibles: int,
        blocked: bool,
        max_per_order: int,
        asset_ids: list = [],
        collection_id: str = None,
        max_per_user: int = None,
        remark: str = None,
    ) -> pack.EditPackDWResponse:
        api = EditPackDWApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = pack.EditPackDWPathParams(uuid=uuid)
        request = pack.EditPackDWDetailParams(
            name=name,
            description=description,
            collectibles=collectibles,
            asset_ids=asset_ids,
            cover=cover,
            collection_id=collection_id,
            blocked=blocked,
            max_per_user=max_per_user,
            max_per_order=max_per_order,
            remark=remark,
        )
        return pack.EditPackDWResponse.parse_raw(b=api.call(path_params=path_params, json=request.dict()).content)

    def create_pack_items_normal(
        self,
        pack_id: str,
        items: list,
    ) -> pack.CreatePackItemsResponse:
        api = CreatePackItemsApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = pack.CreatePackItemsPathParams(pack_id=pack_id)
        request = pack.CreatePackItemsDetailParams(items=items)
        b = api.call(path_params=path_params, json=request.dict())
        return b

    def create_pack_items_abnormal(
        self,
        pack_id: str,
        items: list,
    ) -> pack.CreatePackItemsResponse:
        api = CreatePackItemsApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = pack.CreatePackItemsPathParams(pack_id=pack_id)
        request = pack.CreatePackItemsDetailParams(items=items)
        return pack.CreatePackItemsResponse.parse_raw(b=api.call(path_params=path_params, json=request.dict()).content)
