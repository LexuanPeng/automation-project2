from cdc.qa.apis.crypto_nft.models import NFTRestApi, NFTClientService, create_nft


class GetCollectionsByCreatorApi(NFTRestApi):
    response_type = create_nft.GetCollectionsByCreatorResponse


class GetCreatorWeeklyCreateStatusApi(NFTRestApi):
    response_type = create_nft.GetCreatorWeeklyCreateStatusResponse


class GetAttachmentApi(NFTRestApi):
    response_type = create_nft.GetAttachmentResponse


class CreateAssetApi(NFTRestApi):
    response_type = create_nft.CreateAssetResponse


class CheckoutAssetRecordApi(NFTRestApi):
    response_type = create_nft.CheckoutAssetRecordResponse


class GetCreatorApplicationStatusApi(NFTRestApi):
    response_type = create_nft.GetCreatorApplicationStatusResponse


class MintHistoryApi(NFTRestApi):
    response_type = create_nft.MintHistoryResponse


class GetCrossChainMintFeeQuoteApi(NFTRestApi):
    response_type = create_nft.GetCrossChainMintFeeQuoteResponse


class CreateNftService(NFTClientService):
    def get_collections_by_creator(self, creator_id: str, first: int) -> create_nft.GetCollectionsByCreatorResponse:
        api = GetCollectionsByCreatorApi(host=self.host, _session=self.session)
        request = create_nft.GetCollectionsByCreatorRequest(
            variables=create_nft.GetCollectionsByCreatorRequest.Variables(creatorId=creator_id, first=first)
        )
        return create_nft.GetCollectionsByCreatorResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_creator_weekly_create_status(self, token: str = None) -> create_nft.GetCreatorWeeklyCreateStatusResponse:
        api = GetCreatorWeeklyCreateStatusApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = create_nft.GetCreatorWeeklyCreateStatusRequest()
        return create_nft.GetCreatorWeeklyCreateStatusResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_attachment(self, id: str, token: str = None) -> create_nft.GetAttachmentResponse:
        api = GetAttachmentApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = create_nft.GetAttachmentRequest(variables=create_nft.GetAttachmentRequest.Variables(id=id))
        return create_nft.GetAttachmentResponse.parse_raw(b=api.call(json=request.dict()).content)

    def create_asset(
        self,
        description: str,
        main_id: str,
        name: str,
        categories: list,
        attributes: list,
        collection_id: str,
        copies: int,
        network: str,
        token: str = None,
    ) -> create_nft.CreateAssetResponse:
        api = CreateAssetApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = create_nft.CreateAssetRequest(
            variables=create_nft.CreateAssetRequest.Variables(
                description=description,
                mainId=main_id,
                name=name,
                categories=categories,
                attributes=attributes,
                collectionId=collection_id,
                copies=copies,
                network=network,
            )
        )
        return create_nft.CreateAssetResponse.parse_raw(b=api.call(json=request.dict()).content)

    def checkout_asset_record(
        self, asset_create_record_id: str, kind: str, token: str = None
    ) -> create_nft.CheckoutAssetRecordResponse:
        api = CheckoutAssetRecordApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = create_nft.CheckoutAssetRecordRequest(
            variables=create_nft.CheckoutAssetRecordRequest.Variables(
                assetCreateRecordId=asset_create_record_id,
                kind=kind,
            )
        )
        return create_nft.CheckoutAssetRecordResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_creator_application_status(self, token: str = None) -> create_nft.GetCreatorApplicationStatusResponse:
        api = GetCreatorApplicationStatusApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = create_nft.GetCreatorApplicationStatusRequest()
        return create_nft.GetCreatorApplicationStatusResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_mint_history(self, first: int, skip: int, token: str = None) -> create_nft.MintHistoryResponse:
        api = MintHistoryApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = create_nft.MintHistoryRequest(
            variables=create_nft.MintHistoryRequest.Variables(first=first, skip=skip)
        )
        return create_nft.MintHistoryResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_cross_chain_mint_fee_quote(
        self, asset_create_record_id: str, token: str = None
    ) -> create_nft.GetCrossChainMintFeeQuoteResponse:
        api = GetCrossChainMintFeeQuoteApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = create_nft.GetCrossChainMintFeeQuoteRequest(
            variables=create_nft.GetCrossChainMintFeeQuoteRequest.Variables(assetCreateRecordId=asset_create_record_id)
        )
        return create_nft.GetCrossChainMintFeeQuoteResponse.parse_raw(b=api.call(json=request.dict()).content)
