from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.crypto_nft_admin.models import NFTRestApi, NFTRestService, drops


class GetDropsApi(NFTRestApi):
    path = "/api/asset/drop/list/"
    method = HttpMethods.POST
    request_params_type = drops.GetDropsDetailParams
    response_type = drops.GetDropsResponse


class GetDropsAbnormalApi(NFTRestApi):
    path = "/api/asset/drop/list/"
    method = HttpMethods.POST
    request_params_type = drops.GetDropsDetailParams
    response_type = drops.GetDropsAbnormalResponse


class GetDropsByUuidApi(NFTRestApi):
    def path(self, path_params: drops.GetDropsByUuidPathParams):
        return f"/api/asset/drop/{path_params.uuid}"

    method = HttpMethods.GET
    path_params_type = drops.GetDropsByUuidPathParams
    response_type = drops.GetDropsByUuidResponse


class GetDropsByUuidAbnormalApi(NFTRestApi):
    def path(self, path_params: drops.GetDropsByUuidPathParams):
        return f"/api/asset/drop/{path_params.uuid}"

    method = HttpMethods.GET
    path_params_type = drops.GetDropsByUuidPathParams
    response_type = drops.GetDropsByUuidAbnormalResponse


class CreateDropsApi(NFTRestApi):
    path = "/api/asset/drop/"
    method = HttpMethods.POST
    request_params_type = drops.CreateDropsDetailParams
    response_type = drops.CreateDropsResponse


class EditDropsApi(NFTRestApi):
    def path(self, path_params: drops.EditDropsPathParams):
        return f"/api/asset/drop/{path_params.id}"

    method = HttpMethods.PUT
    path_params_type = drops.EditDropsPathParams
    request_params_type = drops.EditDropsDetailParams
    response_type = drops.EditDropsResponse


class CreateDropsDwApi(NFTRestApi):
    path = "/api/asset/drop/dw"
    method = HttpMethods.POST
    request_params_type = drops.CreateDropsDwDetailParams
    response_type = drops.CreateDropsDwResponse


class EditDropsDwApi(NFTRestApi):
    def path(self, path_params: drops.EditDropsDwPathParams):
        return f"/api/asset/drop/dw/{path_params.id}"

    method = HttpMethods.PUT
    path_params_type = drops.EditDropsDwPathParams
    request_params_type = drops.EditDropsDwDetailParams
    response_type = drops.EditDropsDwResponse


class DropsService(NFTRestService):
    def query_drops(
        self,
        current_page: int,
        page_size: int = None,
        id: str = None,
        name: str = None,
        creator_uuids: list = [],
    ) -> drops.GetDropsResponse:
        api = GetDropsApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = drops.GetDropsDetailParams(
            current_page=current_page, page_size=page_size, id=id, name=name, creator_uuids=creator_uuids
        )
        return drops.GetDropsResponse.parse_raw(b=api.call(json=request.dict()).content)

    def query_drops_abnormal(
        self,
        current_page: int,
        page_size: int = None,
        id: str = None,
        name: str = None,
        creator_uuids: list = [],
    ) -> drops.GetDropsAbnormalResponse:
        api = GetDropsAbnormalApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = drops.GetDropsDetailParams(
            current_page=current_page, page_size=page_size, id=id, name=name, creator_uuids=creator_uuids
        )
        return drops.GetDropsAbnormalResponse.parse_raw(b=api.call(json=request.dict()).content)

    def query_drops_by_uuid(
        self,
        uuid: str,
    ) -> drops.GetDropsByUuidResponse:
        api = GetDropsByUuidApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = drops.GetDropsByUuidPathParams(uuid=uuid)
        return drops.GetDropsByUuidResponse.parse_raw(b=api.call(path_params=path_params).content)

    def query_drops_by_uuid_abnormal(
        self,
        uuid: str,
    ) -> drops.GetDropsByUuidAbnormalResponse:
        api = GetDropsByUuidAbnormalApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = drops.GetDropsByUuidPathParams(uuid=uuid)
        return drops.GetDropsByUuidAbnormalResponse.parse_raw(b=api.call(path_params=path_params).content)

    def create_drops_normal(
        self,
        name: str,
        cover: str,
        creator_info: str,
        description: str,
        start_time: str,
        end_time: str,
        creator_id: str,
        show_collectible: bool = True,
        public_read_only: bool = False,
        video: str = None,
        terms_and_conditions: str = None,
        what_inside_description: str = None,
    ) -> drops.CreateDropsResponse:
        api = CreateDropsApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = drops.CreateDropsDetailParams(
            name=name,
            cover=cover,
            creator_info=creator_info,
            description=description,
            start_time=start_time,
            end_time=end_time,
            creator_id=creator_id,
            show_collectible=show_collectible,
            public_read_only=public_read_only,
            video=video,
            terms_and_conditions=terms_and_conditions,
            what_inside_description=what_inside_description,
        )
        b = api.call(json=request.dict())
        return b

    def create_drops_abnormal(
        self,
        name: str,
        cover: str,
        creator_info: str,
        description: str,
        start_time: str,
        end_time: str,
        creator_id: str,
        show_collectible: bool = True,
        public_read_only: bool = False,
        video: str = None,
        terms_and_conditions: str = None,
        what_inside_description: str = None,
    ) -> drops.CreateDropsResponse:
        api = CreateDropsApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = drops.CreateDropsDetailParams(
            name=name,
            cover=cover,
            creator_info=creator_info,
            description=description,
            start_time=start_time,
            end_time=end_time,
            creator_id=creator_id,
            show_collectible=show_collectible,
            public_read_only=public_read_only,
            video=video,
            terms_and_conditions=terms_and_conditions,
            what_inside_description=what_inside_description,
        )
        return drops.CreateDropsResponse.parse_raw(b=api.call(json=request.dict()).content)

    def edit_drops_normal(
        self,
        id: str,
        name: str,
        creator_info: str,
        creator_id: str,
        description: str,
        start_time: str,
        end_time: str,
        blocked: bool,
        show_collectible: bool,
        public_read_only: bool,
        cover: str = None,
        video: str = None,
        terms_and_conditions: str = None,
        what_inside_description: str = None,
    ) -> drops.EditDropsResponse:
        api = EditDropsApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = drops.EditDropsPathParams(id=id)
        request = drops.EditDropsDetailParams(
            name=name,
            creator_info=creator_info,
            creator_id=creator_id,
            description=description,
            start_time=start_time,
            end_time=end_time,
            blocked=blocked,
            show_collectible=show_collectible,
            public_read_only=public_read_only,
            cover=cover,
            video=video,
            terms_and_conditions=terms_and_conditions,
            what_inside_description=what_inside_description,
        )
        b = api.call(path_params=path_params, json=request.dict())
        return b

    def edit_drops_abnormal(
        self,
        id: str,
        name: str,
        creator_info: str,
        creator_id: str,
        description: str,
        start_time: str,
        end_time: str,
        blocked: bool,
        show_collectible: bool,
        public_read_only: bool,
        cover: str = None,
        video: str = None,
        terms_and_conditions: str = None,
        what_inside_description: str = None,
    ) -> drops.EditDropsResponse:
        api = EditDropsApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = drops.EditDropsPathParams(id=id)
        request = drops.EditDropsDetailParams(
            name=name,
            creator_info=creator_info,
            creator_id=creator_id,
            description=description,
            start_time=start_time,
            end_time=end_time,
            blocked=blocked,
            show_collectible=show_collectible,
            public_read_only=public_read_only,
            cover=cover,
            video=video,
            terms_and_conditions=terms_and_conditions,
            what_inside_description=what_inside_description,
        )
        return drops.EditDropsResponse.parse_raw(b=api.call(path_params=path_params, json=request.dict()).content)

    def create_drops_dw_normal(
        self,
        name: str,
        cover: str,
        creator_info: str,
        description: str,
        start_time: str,
        end_time: str,
        creator_id: str,
        show_collectible: bool = True,
        public_read_only: bool = False,
        video: str = None,
        terms_and_conditions: str = None,
        what_inside_description: str = None,
    ) -> drops.CreateDropsDwResponse:
        api = CreateDropsDwApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = drops.CreateDropsDwDetailParams(
            name=name,
            cover=cover,
            creator_info=creator_info,
            description=description,
            start_time=start_time,
            end_time=end_time,
            creator_id=creator_id,
            show_collectible=show_collectible,
            public_read_only=public_read_only,
            video=video,
            terms_and_conditions=terms_and_conditions,
            what_inside_description=what_inside_description,
        )
        b = api.call(json=request.dict())
        return b

    def create_drops_dw_abnormal(
        self,
        name: str,
        cover: str,
        creator_info: str,
        description: str,
        start_time: str,
        end_time: str,
        creator_id: str,
        show_collectible: bool = True,
        public_read_only: bool = False,
        video: str = None,
        terms_and_conditions: str = None,
        what_inside_description: str = None,
    ) -> drops.CreateDropsDwResponse:
        api = CreateDropsDwApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = drops.CreateDropsDwDetailParams(
            name=name,
            cover=cover,
            creator_info=creator_info,
            description=description,
            start_time=start_time,
            end_time=end_time,
            creator_id=creator_id,
            show_collectible=show_collectible,
            public_read_only=public_read_only,
            video=video,
            terms_and_conditions=terms_and_conditions,
            what_inside_description=what_inside_description,
        )
        return drops.CreateDropsDwResponse.parse_raw(b=api.call(json=request.dict()).content)

    def edit_drops_dw_normal(
        self,
        id: str,
        name: str,
        creator_info: str,
        creator_id: str,
        description: str,
        start_time: str,
        end_time: str,
        blocked: bool,
        show_collectible: bool,
        public_read_only: bool,
        cover: str = None,
        video: str = None,
        terms_and_conditions: str = None,
        what_inside_description: str = None,
    ) -> drops.EditDropsDwResponse:
        api = EditDropsDwApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = drops.EditDropsDwPathParams(id=id)
        request = drops.EditDropsDwDetailParams(
            name=name,
            creator_info=creator_info,
            creator_id=creator_id,
            description=description,
            start_time=start_time,
            end_time=end_time,
            blocked=blocked,
            show_collectible=show_collectible,
            public_read_only=public_read_only,
            cover=cover,
            video=video,
            terms_and_conditions=terms_and_conditions,
            what_inside_description=what_inside_description,
        )
        b = api.call(path_params=path_params, json=request.dict())
        return b

    def edit_drops_dw_abnormal(
        self,
        id: str,
        name: str,
        creator_info: str,
        creator_id: str,
        description: str,
        start_time: str,
        end_time: str,
        blocked: bool,
        show_collectible: bool,
        public_read_only: bool,
        cover: str = None,
        video: str = None,
        terms_and_conditions: str = None,
        what_inside_description: str = None,
    ) -> drops.EditDropsDwResponse:
        api = EditDropsDwApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        path_params = drops.EditDropsDwPathParams(id=id)
        request = drops.EditDropsDwDetailParams(
            name=name,
            creator_info=creator_info,
            creator_id=creator_id,
            description=description,
            start_time=start_time,
            end_time=end_time,
            blocked=blocked,
            show_collectible=show_collectible,
            public_read_only=public_read_only,
            cover=cover,
            video=video,
            terms_and_conditions=terms_and_conditions,
            what_inside_description=what_inside_description,
        )
        return drops.EditDropsDwResponse.parse_raw(b=api.call(path_params=path_params, json=request.dict()).content)
