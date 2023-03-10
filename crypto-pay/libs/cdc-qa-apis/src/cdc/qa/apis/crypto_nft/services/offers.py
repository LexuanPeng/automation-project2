from cdc.qa.apis.crypto_nft.models import NFTRestApi, NFTClientService, offers


class CreateOfferApi(NFTRestApi):
    response_type = offers.CreateOfferResponse


class GetOfferApi(NFTRestApi):
    response_type = offers.GetOfferResponse


class GetOffersMadeApi(NFTRestApi):
    response_type = offers.GetOffersMadeResponse


class GetOffersRecievedApi(NFTRestApi):
    response_type = offers.GetOffersRecievedResponse


class AcceptOfferApi(NFTRestApi):
    response_type = offers.AcceptOfferResponse


class GetMyWalletsApi(NFTRestApi):
    response_type = offers.GetMyWalletsResponse


class AccountBalanceQueryApi(NFTRestApi):
    response_type = offers.AccountBalanceQueryResponse


class RejectOfferApi(NFTRestApi):
    response_type = offers.RejectOfferResponse


class OffersService(NFTClientService):
    def create_offer(self, edition_id: str, amount_decimal: str, token: str = None) -> offers.CreateOfferResponse:
        api = CreateOfferApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = offers.CreateOfferRequest(
            variables=offers.CreateOfferRequest.Variables(editionId=edition_id, amountDecimal=amount_decimal)
        )
        return offers.CreateOfferResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_offer(self, offer_id: str, token: str = None) -> offers.GetOfferResponse:
        api = GetOfferApi(host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token)
        request = offers.GetOfferRequest(variables=offers.GetOfferRequest.Variables(offerId=offer_id))
        return offers.GetOfferResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_offer_made(self, first: int, skip: int, token: str = None) -> offers.GetOffersMadeResponse:
        api = GetOffersMadeApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = offers.GetOffersMadeRequest(variables=offers.GetOffersMadeRequest.Variables(first=first, skip=skip))
        return offers.GetOffersMadeResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_offer_recieved(self, first: int, skip: int, token: str = None) -> offers.GetOffersRecievedResponse:
        api = GetOffersRecievedApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = offers.GetOffersRecievedRequest(
            variables=offers.GetOffersRecievedRequest.Variables(first=first, skip=skip)
        )
        return offers.GetOffersRecievedResponse.parse_raw(b=api.call(json=request.dict()).content)

    def accept_offer(self, id: str, token: str = None) -> offers.AcceptOfferResponse:
        api = AcceptOfferApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = offers.AcceptOfferRequest(variables=offers.AcceptOfferRequest.Variables(id=id))
        return offers.AcceptOfferResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_my_wallets(self, token: str = None) -> offers.GetMyWalletsResponse:
        api = GetMyWalletsApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = offers.GetMyWalletsRequest()
        return offers.GetMyWalletsResponse.parse_raw(b=api.call(json=request.dict()).content)

    def account_balance_query(self, token: str = None) -> offers.AccountBalanceQueryResponse:
        api = AccountBalanceQueryApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = offers.AccountBalanceQueryRequest()
        return offers.AccountBalanceQueryResponse.parse_raw(b=api.call(json=request.dict()).content)

    def reject_offer(self, id: str, token: str = None) -> offers.RejectOfferResponse:
        api = RejectOfferApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = offers.RejectOfferRequest(variables=offers.RejectOfferRequest.Variables(id=id))
        return offers.RejectOfferResponse.parse_raw(b=api.call(json=request.dict()).content)
