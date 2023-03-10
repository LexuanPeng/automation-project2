from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.crypto_nft_admin.models import NFTRestApi, NFTRestService, dropasset


class GetDropAssetApi(NFTRestApi):
    path = "/api/asset/drop-asset/list/"
    method = HttpMethods.POST
    request_params_type = dropasset.GetDropAssetDetailParams
    response_type = dropasset.GetDropAssetResponse


class GetDropAssetAbnormalApi(NFTRestApi):
    path = "/api/asset/drop-asset/list/"
    method = HttpMethods.POST
    request_params_type = dropasset.GetDropAssetDetailParams
    response_type = dropasset.GetDropAssetAbnormalResponse


class GetDropAssetByIdApi(NFTRestApi):
    def path(self, path_params: dropasset.GetDropAssetByIdPathParams):
        return f"/api/asset/drop-asset/{path_params.id}"

    method = HttpMethods.GET
    path_params_type = dropasset.GetDropAssetByIdPathParams
    response_type = dropasset.GetDropAssetByIdResponse


class GetDropAssetByIdAbnormalApi(NFTRestApi):
    def path(self, path_params: dropasset.GetDropAssetByIdPathParams):
        return f"/api/asset/drop-asset/{path_params.id}"

    method = HttpMethods.GET
    path_params_type = dropasset.GetDropAssetByIdPathParams
    response_type = dropasset.GetDropAssetByIdAbnormalResponse


class CreateDropAssetDwApi(NFTRestApi):
    path = "/api/asset/drop-asset/dw"
    method = HttpMethods.POST
    request_params_type = dropasset.CreateDropAssetDwDetailParams
    response_type = dropasset.CreateDropAssetDwResponse


class EditDropAssetDwApi(NFTRestApi):
    def path(self, path_params: dropasset.EditDropAssetDwPathParams):
        return f"/api/asset/drop-asset/dw/{path_params.id}"

    method = HttpMethods.PUT
    path_params_type = dropasset.EditDropAssetDwPathParams
    request_params_type = dropasset.EditDropAssetDwDetailParams
    response_type = dropasset.EditDropAssetDwResponse


class DropAssetService(NFTRestService):
    def query_dropasset(
        self,
        current_page: int,
        page_size: int = None,
        id: str = None,
        name: str = None,
        creator_uuids: list = [],
    ) -> dropasset.GetDropAssetResponse:
        api = GetDropAssetApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = dropasset.GetDropAssetDetailParams(
            current_page=current_page,
            page_size=page_size,
            id=id,
            name=name,
            creator_uuids=creator_uuids,
        )
        return dropasset.GetDropAssetResponse.parse_raw(b=api.call(json=request.dict()).content)

    def query_dropasset_abnormal(
        self,
        current_page: int,
        page_size: int = None,
        id: str = None,
        name: str = None,
        creator_uuids: list = [],
    ) -> dropasset.GetDropAssetAbnormalResponse:
        api = GetDropAssetAbnormalApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = dropasset.GetDropAssetDetailParams(
            current_page=current_page,
            page_size=page_size,
            id=id,
            name=name,
            creator_uuids=creator_uuids,
        )
        return dropasset.GetDropAssetAbnormalResponse.parse_raw(b=api.call(json=request.dict()).content)

    def query_dropasset_by_id(
        self,
        id: str,
    ) -> dropasset.GetDropAssetByIdResponse:
        api = GetDropAssetByIdApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = dropasset.GetDropAssetByIdPathParams(id=id)
        return dropasset.GetDropAssetByIdResponse.parse_raw(b=api.call(path_params=path_params).content)

    def query_dropasset_by_id_abnormal(
        self,
        id: str,
    ) -> dropasset.GetDropAssetByIdAbnormalResponse:
        api = GetDropAssetByIdAbnormalApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = dropasset.GetDropAssetByIdPathParams(id=id)
        return dropasset.GetDropAssetByIdAbnormalResponse.parse_raw(b=api.call(path_params=path_params).content)

    def create_dropasset_dw_normal(
        self,
        name: str,
        cover: str,
        main: str,
        description: str,
        creator_id: str,
        type: int,
        royalty: int,
        collection_id: str = None,
        editions: int = 1,
        category_list: list = [],
        properties: list = [],
        on_chain: bool = False,
    ) -> dropasset.CreateDropAssetDwResponse:
        api = CreateDropAssetDwApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = dropasset.CreateDropAssetDwDetailParams(
            name=name,
            cover=cover,
            main=main,
            description=description,
            creator_id=creator_id,
            type=type,
            royalty=royalty,
            collection_id=collection_id,
            editions=editions,
            category_list=category_list,
            properties=properties,
            on_chain=on_chain,
        )
        b = api.call(json=request.dict())
        return b

    def create_dropasset_dw_abnormal(
        self,
        name: str,
        cover: str,
        main: str,
        description: str,
        creator_id: str,
        type: int,
        royalty: int,
        collection_id: str = None,
        editions: int = 1,
        category_list: list = [],
        properties: list = [],
        on_chain: bool = False,
    ) -> dropasset.CreateDropAssetDwResponse:
        api = CreateDropAssetDwApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = dropasset.CreateDropAssetDwDetailParams(
            name=name,
            cover=cover,
            main=main,
            description=description,
            creator_id=creator_id,
            type=type,
            royalty=royalty,
            collection_id=collection_id,
            editions=editions,
            category_list=category_list,
            properties=properties,
            on_chain=on_chain,
        )
        return dropasset.CreateDropAssetDwResponse.parse_raw(b=api.call(json=request.dict()).content)

    def edit_dropasset_dw_normal(
        self,
        id: str,
        name: str,
        main: str,
        description: str,
        type: int,
        royalty: int,
        collection_id: str = None,
        cover: str = None,
        auction_max_end_date: str = None,
        remark: str = None,
        blocked: bool = False,
        showcopiesincirculation: bool = False,
        editions: int = 1,
        category: list = [],
        properties: list = [],
        on_chain: bool = False,
        withdrawal: bool = False,
    ) -> dropasset.EditDropAssetDwResponse:
        api = EditDropAssetDwApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = dropasset.EditDropAssetDwPathParams(id=id)
        request = dropasset.EditDropAssetDwDetailParams(
            name=name,
            cover=cover,
            main=main,
            description=description,
            type=type,
            royalty=royalty,
            collection_id=collection_id,
            auction_max_end_date=auction_max_end_date,
            remark=remark,
            blocked=blocked,
            showcopiesincirculation=showcopiesincirculation,
            editions=editions,
            category=category,
            properties=properties,
            on_chain=on_chain,
            withdrawal=withdrawal,
        )
        b = api.call(
            path_params=path_params,
            json=request.dict(),
        )
        return b

    def edit_dropasset_dw_abnormal(
        self,
        id: str,
        name: str,
        main: str,
        description: str,
        type: int,
        royalty: int,
        collection_id: str = None,
        cover: str = None,
        auction_max_end_date: str = None,
        remark: str = None,
        blocked: bool = False,
        showcopiesincirculation: bool = False,
        editions: int = 1,
        category: list = [],
        properties: list = [],
        on_chain: bool = False,
        withdrawal: bool = False,
    ) -> dropasset.EditDropAssetDwResponse:
        api = EditDropAssetDwApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = dropasset.EditDropAssetDwPathParams(id=id)
        request = dropasset.EditDropAssetDwDetailParams(
            name=name,
            cover=cover,
            main=main,
            description=description,
            type=type,
            royalty=royalty,
            collection_id=collection_id,
            auction_max_end_date=auction_max_end_date,
            remark=remark,
            blocked=blocked,
            showcopiesincirculation=showcopiesincirculation,
            editions=editions,
            category=category,
            properties=properties,
            on_chain=on_chain,
            withdrawal=withdrawal,
        )
        return dropasset.EditDropAssetDwResponse.parse_raw(
            b=api.call(
                path_params=path_params,
                json=request.dict(),
            ).content
        )
