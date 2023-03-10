from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.crypto_nft_admin.models import NFTRestApi, NFTRestService, collection


class CreateCollectionApi(NFTRestApi):
    path = "/api/asset/collection/"
    method = HttpMethods.POST
    request_params_type = collection.CreateCollectionDetailParams
    response_type = collection.CreateCollectionResponse


class EditCollectionApi(NFTRestApi):
    def path(self, path_params: collection.EditCollectionPathParams):
        return f"path = /api/asset/collection/{path_params.id}"

    method = HttpMethods.PUT
    path_params_type = collection.EditCollectionPathParams
    request_params_type = collection.EditCollectionDetailParams
    response_type = collection.EditCollectionResponse


class CollectionService(NFTRestService):
    def create_collection_normal(
        self,
        name: str,
        logo: str,
        banner: str,
        description: str,
        creator_id: str,
        category: list = [],
    ) -> collection.CreateCollectionResponse:
        api = CreateCollectionApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = collection.CreateCollectionDetailParams(
            name=name,
            logo=logo,
            banner=banner,
            description=description,
            creator_id=creator_id,
            category=category,
        )
        b = api.call(json=request.dict())
        return b

    def create_collection_abnormal(
        self,
        name: str,
        logo: str,
        banner: str,
        description: str,
        creator_id: str,
        category: list = [],
    ) -> collection.CreateCollectionResponse:
        api = CreateCollectionApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = collection.CreateCollectionDetailParams(
            name=name,
            logo=logo,
            banner=banner,
            description=description,
            creator_id=creator_id,
            category=category,
        )
        return collection.CreateCollectionResponse.parse_raw(b=api.call(json=request.dict()).content)

    def edit_collection_normal(
        self,
        id: str,
        description: str,
        name: str = None,
        logo: str = None,
        banner: str = None,
        category: list = [],
    ) -> collection.EditCollectionResponse:
        api = EditCollectionApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = collection.EditCollectionPathParams(id=id)
        request = collection.EditCollectionDetailParams(
            description=description,
            name=name,
            logo=logo,
            banner=banner,
            category=category,
        )
        b = api.call(
            path_params=path_params,
            json=request.dict(),
        )
        return b

    def edit_collection_abnormal(
        self,
        id: str,
        description: str,
        name: str = None,
        logo: str = None,
        banner: str = None,
        category: list = [],
    ) -> collection.EditCollectionResponse:
        api = EditCollectionApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = collection.EditCollectionPathParams(id=id)
        request = collection.EditCollectionDetailParams(
            description=description,
            name=name,
            logo=logo,
            banner=banner,
            category=category,
        )
        return collection.EditCollectionResponse.parse_raw(
            b=api.call(
                path_params=path_params,
                json=request.dict(),
            ).content
        )
