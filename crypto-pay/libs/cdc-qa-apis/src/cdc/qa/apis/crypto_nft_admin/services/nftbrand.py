from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.crypto_nft_admin.models import NFTRestApi, NFTRestService, nftbrand


class GetBrandListApi(NFTRestApi):
    path = "/api/asset/brand/list/"
    method = HttpMethods.GET
    request_params_type = nftbrand.GetBrandListParams
    response_type = nftbrand.GetBrandListResponse


class GetBrandListAbnormalApi(NFTRestApi):
    path = "/api/asset/brand/list/"
    method = HttpMethods.GET
    request_params_type = nftbrand.GetBrandListParams
    response_type = nftbrand.GetBrandListAbnormalResponse


class GetBrandDetailApi(NFTRestApi):
    def path(self, path_params: nftbrand.GetBrandDetailPathParams):
        return f"path = /api/asset/brand/{path_params.id}"

    method = HttpMethods.GET
    path_params_type = nftbrand.GetBrandDetailPathParams
    response_type = nftbrand.GetBrandDetailResponse


class GetBrandDetailAbnormalApi(NFTRestApi):
    def path(self, path_params: nftbrand.GetBrandDetailPathParams):
        return f"path = /api/asset/brand/{path_params.id}"

    method = HttpMethods.GET
    path_params_type = nftbrand.GetBrandDetailPathParams
    response_type = nftbrand.GetBrandDetailAbnormalResponse


class CreateBrandApi(NFTRestApi):
    path = "/api/asset/brand/"
    method = HttpMethods.POST
    request_params_type = nftbrand.CreateBrandParams
    response_type = nftbrand.CreateBrandResponse


class EditBrandApi(NFTRestApi):
    def path(self, path_params: nftbrand.EditBrandPathParams):
        return f"path = /api/asset/brand/{path_params.id}"

    method = HttpMethods.PUT
    path_params_type = nftbrand.EditBrandPathParams
    request_params_type = nftbrand.EditBrandParams
    response_type = nftbrand.EditBrandResponse


class GetCollectionBookListApi(NFTRestApi):
    path = "/api/asset/brand/list/"
    method = HttpMethods.GET
    request_params_type = nftbrand.GetCollectionBookListParams
    response_type = nftbrand.GetCollectionBookListResponse


class GetCollectionBookDetailApi(NFTRestApi):
    def path(self, path_params: nftbrand.GetCollectionBookDetailPathParams):
        return f"path = /api/asset/brand/{path_params.id}"

    method = HttpMethods.GET
    path_params_type = nftbrand.GetCollectionBookDetailPathParams
    response_type = nftbrand.GetCollectionBookDetailResponse


class CreateCollectionBookApi(NFTRestApi):
    path = "/api/asset/collection-book/"
    method = HttpMethods.POST
    request_params_type = nftbrand.CreateCollectionBookParams
    response_type = nftbrand.CreateCollectionBookResponse


class EditCollectionBookApi(NFTRestApi):
    def path(self, path_params: nftbrand.EditCollectionBookPathParams):
        return f"path = /api/asset/collection-book/{path_params.id}"

    method = HttpMethods.PUT
    path_params_type = nftbrand.EditCollectionBookPathParams
    request_params_type = nftbrand.EditCollectionBookParams
    response_type = nftbrand.EditCollectionBookResponse


class AttachSegmentToCollectionBookApi(NFTRestApi):
    def path(self, path_params: nftbrand.AttachSegmentToCollectionBookPathParams):
        return f"path = /api/asset/collection-book/{path_params.id}/segment/"

    method = HttpMethods.POST
    path_params_type = nftbrand.AttachSegmentToCollectionBookPathParams
    request_params_type = nftbrand.AttachSegmentToCollectionBookParams
    response_type = nftbrand.AttachSegmentToCollectionBookResponse


class UpdateAssetPlaceholderApi(NFTRestApi):
    def path(self, path_params: nftbrand.UpdateAssetPlaceholderPathParams):
        return f"path = /api/asset/collection-book/{path_params.id}/asset/"

    method = HttpMethods.PUT
    path_params_type = nftbrand.UpdateAssetPlaceholderPathParams
    request_params_type = nftbrand.UpdateAssetPlaceholderParams
    response_type = nftbrand.UpdateAssetPlaceholderResponse


class BrandService(NFTRestService):
    def query_brand_list(
        self,
        current_page: int,
        page_size: int = 20,
    ) -> nftbrand.GetBrandListResponse:
        api = GetBrandListApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = nftbrand.GetBrandListParams(
            current_page=current_page,
            page_size=page_size,
        )
        return nftbrand.GetBrandListResponse.parse_raw(b=api.call(json=request.dict()).content)

    def query_brand_list_abnormal(
        self,
        current_page: int,
        page_size: int = 20,
    ) -> nftbrand.GetBrandListAbnormalResponse:
        api = GetBrandListAbnormalApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = nftbrand.GetBrandListParams(
            current_page=current_page,
            page_size=page_size,
        )
        return nftbrand.GetBrandListAbnormalResponse.parse_raw(b=api.call(json=request.dict()).content)

    def query_brand_detail(
        self,
        id: str,
    ) -> nftbrand.GetBrandDetailResponse:
        api = GetBrandDetailApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = nftbrand.GetBrandDetailPathParams(id=id)
        return nftbrand.GetBrandDetailResponse.parse_raw(b=api.call(path_params=path_params).content)

    def query_brand_detail_abnormal(
        self,
        id: str,
    ) -> nftbrand.GetBrandDetailAbnormalResponse:
        api = GetBrandDetailAbnormalApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = nftbrand.GetBrandDetailPathParams(id=id)
        return nftbrand.GetBrandDetailAbnormalResponse.parse_raw(b=api.call(path_params=path_params).content)

    def create_brand_normal(
        self,
        name: str,
        creator_id: str,
        slug: str,
        cover: str,
        blocked: bool,
        description: str,
        collection_book_id: str = None,
        drops: list = [],
    ) -> nftbrand.CreateBrandResponse:
        api = CreateBrandApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = nftbrand.CreateBrandParams(
            name=name,
            creator_id=creator_id,
            slug=slug,
            cover=cover,
            blocked=blocked,
            description=description,
            collection_book_id=collection_book_id,
            drops=drops,
        )
        b = api.call(json=request.dict())
        return b

    def create_brand_abnormal(
        self,
        name: str,
        creator_id: str,
        slug: str,
        cover: str,
        blocked: bool,
        description: str,
        collection_book_id: str = None,
        drops: list = [],
    ) -> nftbrand.CreateBrandResponse:
        api = CreateBrandApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = nftbrand.CreateBrandParams(
            name=name,
            creator_id=creator_id,
            slug=slug,
            cover=cover,
            blocked=blocked,
            description=description,
            collection_book_id=collection_book_id,
            drops=drops,
        )
        return nftbrand.CreateBrandResponse.parse_raw(b=api.call(json=request.dict()).content)

    def edit_brand_normal(
        self,
        id: str,
        name: str,
        slug: str,
        cover: str,
        blocked: bool,
        description: str,
        collection_book_id: str = None,
        drops: list = [],
    ) -> nftbrand.EditBrandResponse:
        api = EditBrandApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = nftbrand.EditBrandPathParams(id=id)
        request = nftbrand.EditBrandDetailParams(
            name=name,
            slug=slug,
            cover=cover,
            blocked=blocked,
            description=description,
            collection_book_id=collection_book_id,
            drops=drops,
        )
        b = api.call(
            path_params=path_params,
            json=request.dict(),
        )
        return b

    def edit_brand_abnormal(
        self,
        id: str,
        name: str,
        slug: str,
        cover: str,
        blocked: bool,
        description: str,
        collection_book_id: str = None,
        drops: list = [],
    ) -> nftbrand.EditBrandResponse:
        api = EditBrandApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = nftbrand.EditBrandPathParams(id=id)
        request = nftbrand.EditBrandDetailParams(
            name=name,
            slug=slug,
            cover=cover,
            blocked=blocked,
            description=description,
            collection_book_id=collection_book_id,
            drops=drops,
        )
        return nftbrand.EditBrandResponse.parse_raw(
            b=api.call(
                path_params=path_params,
                json=request.dict(),
            ).content
        )

    def query_collection_book_list(
        self,
        current_page: int,
        page_size: int = 20,
        name: str = None,
    ) -> nftbrand.GetCollectionBookListResponse:
        api = GetCollectionBookListApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = nftbrand.GetCollectionBookListParams(
            current_page=current_page,
            page_size=page_size,
            name=name,
        )
        return nftbrand.GetCollectionBookListResponse.parse_raw(b=api.call(json=request.dict()).content)

    def query_collection_book_detail(
        self,
        id: str,
    ) -> nftbrand.GetCollectionBookDetailResponse:
        api = GetCollectionBookDetailApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = nftbrand.GetCollectionBookDetailPathParams(id=id)
        return nftbrand.GetCollectionBookDetailResponse.parse_raw(b=api.call(path_params=path_params).content)

    def create_collection_book_normal(
        self,
        name: str,
        display_name: str,
        description: str,
        cta_name: str,
        creator_id: str,
        active: bool,
        cover: str = None,
    ) -> nftbrand.CreateCollectionBookResponse:
        api = CreateCollectionBookApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = nftbrand.CreateCollectionBookParams(
            name=name,
            display_name=display_name,
            description=description,
            cta_name=cta_name,
            creator_id=creator_id,
            active=active,
            cover=cover,
        )
        b = api.call(json=request.dict())
        return b

    def create_collection_book_abnormal(
        self,
        name: str,
        display_name: str,
        description: str,
        cta_name: str,
        creator_id: str,
        active: bool,
        cover: str = None,
    ) -> nftbrand.CreateCollectionBookResponse:
        api = CreateCollectionBookApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = nftbrand.CreateCollectionBookParams(
            name=name,
            display_name=display_name,
            description=description,
            cta_name=cta_name,
            creator_id=creator_id,
            active=active,
            cover=cover,
        )
        return nftbrand.CreateCollectionBookResponse.parse_raw(b=api.call(json=request.dict()).content)

    def edit_collection_book_normal(
        self,
        id: str,
        name: str = None,
        display_name: str = None,
        description: str = None,
        cta_name: str = None,
        active: bool = None,
        cover: str = None,
    ) -> nftbrand.EditCollectionBookResponse:
        api = EditCollectionBookApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = nftbrand.EditCollectionBookPathParams(id=id)
        request = nftbrand.EditCollectionBookDetailParams(
            name=name,
            display_name=display_name,
            description=description,
            cta_name=cta_name,
            active=active,
            cover=cover,
        )
        b = api.call(
            path_params=path_params,
            json=request.dict(),
        )
        return b

    def edit_collection_book_abnormal(
        self,
        id: str,
        name: str = None,
        display_name: str = None,
        description: str = None,
        cta_name: str = None,
        active: bool = None,
        cover: str = None,
    ) -> nftbrand.EditCollectionBookResponse:
        api = EditCollectionBookApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = nftbrand.EditCollectionBookPathParams(id=id)
        request = nftbrand.EditCollectionBookDetailParams(
            name=name,
            display_name=display_name,
            description=description,
            cta_name=cta_name,
            active=active,
            cover=cover,
        )
        return nftbrand.EditCollectionBookResponse.parse_raw(
            b=api.call(
                path_params=path_params,
                json=request.dict(),
            ).content
        )

    def attach_segment_to_collection_book_normal(
        self,
        id: str,
        name: str,
        active: bool,
        placeholder: str,
        assets: list = [],
    ) -> nftbrand.AttachSegmentToCollectionBookResponse:
        api = AttachSegmentToCollectionBookApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = nftbrand.AttachSegmentToCollectionBookPathParams(id=id)
        request = nftbrand.AttachSegmentToCollectionBookParams(
            name=name,
            active=active,
            placeholder=placeholder,
            assets=assets,
        )
        b = api.call(
            path_params=path_params,
            json=request.dict(),
        )
        return b

    def attach_segment_to_collection_book_abnormal(
        self,
        id: str,
        name: str,
        active: bool,
        placeholder: str,
        assets: list = [],
    ) -> nftbrand.AttachSegmentToCollectionBookResponse:
        api = AttachSegmentToCollectionBookApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = nftbrand.AttachSegmentToCollectionBookPathParams(id=id)
        request = nftbrand.AttachSegmentToCollectionBookParams(
            name=name,
            active=active,
            placeholder=placeholder,
            assets=assets,
        )
        return nftbrand.AttachSegmentToCollectionBookResponse.parse_raw(
            b=api.call(
                path_params=path_params,
                json=request.dict(),
            ).content
        )

    def update_asset_placeholder_normal(
        self,
        id: str,
        name: str,
        active: bool,
        placeholder: str,
        assets: list = [],
    ) -> nftbrand.UpdateAssetPlaceholderResponse:
        api = UpdateAssetPlaceholderApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = nftbrand.UpdateAssetPlaceholderPathParams(id=id)
        request = nftbrand.UpdateAssetPlaceholderParams(
            name=name,
            active=active,
            placeholder=placeholder,
            assets=assets,
        )
        b = api.call(
            path_params=path_params,
            json=request.dict(),
        )
        return b

    def update_asset_placeholder_abnormal(
        self,
        id: str,
        name: str,
        active: bool,
        placeholder: str,
        assets: list = [],
    ) -> nftbrand.UpdateAssetPlaceholderResponse:
        api = UpdateAssetPlaceholderApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = nftbrand.UpdateAssetPlaceholderPathParams(id=id)
        request = nftbrand.UpdateAssetPlaceholderParams(
            name=name,
            active=active,
            placeholder=placeholder,
            assets=assets,
        )
        return nftbrand.UpdateAssetPlaceholderResponse.parse_raw(
            b=api.call(
                path_params=path_params,
                json=request.dict(),
            ).content
        )
