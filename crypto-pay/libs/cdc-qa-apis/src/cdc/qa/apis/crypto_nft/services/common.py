import random
import string
import json

from requests_toolbelt import MultipartEncoder
from cdc.qa.apis.crypto_nft import graphql
from cdc.qa.apis.crypto_nft.models import NFTRestApi, NFTClientService, common


class GetCreditCardsApi(NFTRestApi):
    response_type = common.GetCreditCardsResponse


class CreateIXOPaymentApi(NFTRestApi):
    response_type = common.CreateIXOPaymentResponse


class PreauthIXOPaymentApi(NFTRestApi):
    response_type = common.PreauthIXOPaymentResponse


class CaptureIXOPaymentApi(NFTRestApi):
    response_type = common.CaptureIXOPaymentResponse


class PaidCheckoutsApi(NFTRestApi):
    response_type = common.PaidCheckoutsResponse


class GetCategoriesApi(NFTRestApi):
    response_type = common.GetCategoriesResponse


class GetBrandsApi(NFTRestApi):
    response_type = common.GetBrandsResponse


class GetPlatformFeeApi(NFTRestApi):
    response_type = common.GetPlatformFeeResponse


class CreateCheckoutApi(NFTRestApi):
    response_type = common.CreateCheckoutResponse


class CreateAndCaptureAccountPaymentApi(NFTRestApi):
    response_type = common.CreateAndCaptureAccountPaymentResponse


class CheckoutApi(NFTRestApi):
    response_type = common.CheckoutResponse


class GetCroMintFeeApi(NFTRestApi):
    response_type = common.GetCroMintFeeResponse


class GetUserCardTierApi(NFTRestApi):
    response_type = common.GetUserCardTierResponse


class GetMeApi(NFTRestApi):
    response_type = common.GetMeResponse


class GetUserCardStakeApi(NFTRestApi):
    response_type = common.GetUserCardStakeResponse


class CreateAttachmentApi(NFTRestApi):
    response_type = common.CreateAttachmentResponse


class PlaceBidMutationApi(NFTRestApi):
    response_type = common.PlaceBidMutationResponse


class GetCollectionApi(NFTRestApi):
    response_type = common.GetCollectionResponse


class GetBiddingHistoryApi(NFTRestApi):
    response_type = common.GetBiddingHistoryResponse


class DeleteCreditCardApi(NFTRestApi):
    response_type = common.DeleteCreditCardResponse


class GetTopCollectiblesApi(NFTRestApi):
    response_type = common.GetTopCollectiblesResponse


class CheckoutAmountApi(NFTRestApi):
    response_type = common.CheckoutAmountResponse


class CommonService(NFTClientService):
    def get_brands(self) -> common.GetBrandsResponse:
        api = GetBrandsApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = common.GetBrandsRequest()
        return common.GetBrandsResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_flat_form_fee(self, token: str = None) -> common.GetPlatformFeeResponse:
        api = GetPlatformFeeApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = common.GetPlatformFeeRequest()
        return common.GetPlatformFeeResponse.parse_raw(b=api.call(json=request.dict()).content)

    def create_checkout(
        self, kind: str, listing_id: str = "", offer_id: str = "", quantity: int = 1, token: str = None
    ) -> common.CreateCheckoutResponse:
        api = CreateCheckoutApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = common.CreateCheckoutRequest(
            variables=common.CreateCheckoutRequest.Variables(
                kind=kind, listingId=listing_id, offerId=offer_id, quantity=quantity
            )
        )
        return common.CreateCheckoutResponse.parse_raw(b=api.call(json=request.dict()).content)

    def create_and_capture_account_payment(
        self, checkout_id: str, token: str = None
    ) -> common.CreateAndCaptureAccountPaymentResponse:
        api = CreateAndCaptureAccountPaymentApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = common.CreateAndCaptureAccountPaymentRequest(
            variables=common.CreateAndCaptureAccountPaymentRequest.Variables(checkoutId=checkout_id)
        )
        return common.CreateAndCaptureAccountPaymentResponse.parse_raw(b=api.call(json=request.dict()).content)

    def checkout(self, id: str, token: str = None) -> common.CheckoutResponse:
        api = CheckoutApi(host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token)
        request = common.CheckoutRequest(variables=common.CheckoutRequest.Variables(id=id))
        return common.CheckoutResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_cro_mint_fee(self, token: str = None) -> common.GetCroMintFeeResponse:
        api = GetCroMintFeeApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = common.GetCroMintFeeRequest()
        return common.GetCroMintFeeResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_user_card_tier(self, id: str, token: str = None) -> common.GetUserCardTierResponse:
        api = GetUserCardTierApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = common.GetUserCardTierRequest(variables=common.GetUserCardTierRequest.Variables(id=id))
        return common.GetUserCardTierResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_me(self, token: str = None) -> common.GetMeResponse:
        api = GetMeApi(host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token)
        request = common.GetMeRequest()
        return common.GetMeResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_user_card_stake(self, id: str, token: str = None) -> common.GetUserCardStakeResponse:
        api = GetUserCardStakeApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = common.GetUserCardStakeRequest(variables=common.GetUserCardStakeRequest.Variables(id=id))
        return common.GetUserCardStakeResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_credit_cards(self) -> common.GetCreditCardsResponse:
        api = GetCreditCardsApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = common.GetCreditCardsRequest()
        return common.GetCreditCardsResponse.parse_raw(b=api.call(json=request.dict()).content)

    def create_ixo_payment(self, params: dict) -> common.CreateIXOPaymentResponse:
        api = CreateIXOPaymentApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = common.CreateIXOPaymentRequest(variables=common.CreateIXOPaymentRequest.Variables(**params))
        return common.CreateIXOPaymentResponse.parse_raw(b=api.call(json=request.dict()).content)

    def preauth_ixo_payment(self, params: dict) -> common.PreauthIXOPaymentResponse:
        api = PreauthIXOPaymentApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = common.PreauthIXOPaymentRequest(variables=common.PreauthIXOPaymentRequest.Variables(**params))
        return common.PreauthIXOPaymentResponse.parse_raw(b=api.call(json=request.dict()).content)

    def capture_ixo_payment(self, params: dict) -> common.CaptureIXOPaymentResponse:
        api = CaptureIXOPaymentApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = common.CaptureIXOPaymentRequest(variables=common.CaptureIXOPaymentRequest.Variables(**params))
        return common.CaptureIXOPaymentResponse.parse_raw(b=api.call(json=request.dict()).content)

    def paid_checkouts(self, params: dict) -> common.PaidCheckoutsResponse:
        api = PaidCheckoutsApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = common.PaidCheckoutsRequest(variables=common.PaidCheckoutsRequest.Variables(**params))
        return common.PaidCheckoutsResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_categories(self, params: dict) -> common.GetCategoriesResponse:
        api = GetCategoriesApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = common.GetCategoriesRequest(variables=common.GetCategoriesRequest.Variables(**params))
        return common.GetCategoriesResponse.parse_raw(b=api.call(json=request.dict()).content)

    def create_attachment(self, params: dict, file: set) -> common.CreateAttachmentResponse:
        """
        @nature: nature name
        @file: (file name, file object, file type)
        return common.CreateAttachmentResponse object
        """
        api = CreateAttachmentApi(host=self.host, _session=self.session, nft_token=self.nft_token)

        boundary = "----WebKitFormBoundary" + "".join(random.sample(string.ascii_letters + string.digits, 16))
        ops = {
            "operationName": "CreateAttachment",
            "variables": params,
            "query": graphql.common.CreateAttachment,
        }
        map = {"i": ["variables.upload"]}
        fields = {
            "operations": json.dumps(ops),
            "map": json.dumps(map),
            "i": file,
        }
        m = MultipartEncoder(fields=fields, boundary=boundary)
        headers = {"Content-Type": m.content_type, "authorization": self.nft_token}
        return common.CreateAttachmentResponse.parse_raw(b=api.call(data=m, headers=headers).content)

    def place_bid_mutation(self, listing_id: str, bid_price: str) -> common.PlaceBidMutationResponse:
        api = PlaceBidMutationApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = common.PlaceBidMutationRequest(
            variables=common.PlaceBidMutationRequest.Variables(listingId=listing_id, bidPriceDecimal=bid_price)
        )
        return common.PlaceBidMutationResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_collection(self, collection_id: str, token: str = None) -> common.GetCollectionResponse:
        api = PlaceBidMutationApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = common.GetCollectionRequest(
            variables=common.GetCollectionRequest.Variables(collectionId=collection_id)
        )
        return common.GetCollectionResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_bidding_history(self, listing_id: str) -> common.GetBiddingHistoryResponse:
        api = GetBiddingHistoryApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = common.GetBiddingHistoryRequest(
            variables=common.GetBiddingHistoryRequest.Variables(listingId=listing_id)
        )
        return common.GetBiddingHistoryResponse.parse_raw(b=api.call(json=request.dict()).content)

    def delete_credit_card(self, card_id: str) -> common.DeleteCreditCardResponse:
        api = DeleteCreditCardApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = common.DeleteCreditCardRequest(variables=common.DeleteCreditCardRequest.Variables(cardId=card_id))
        return common.DeleteCreditCardResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_top_collectibles(self, params: dict) -> common.GetTopCollectiblesResponse:
        api = GetTopCollectiblesApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = common.GetTopCollectiblesRequest(variables=common.GetTopCollectiblesRequest.Variables(**params))
        return common.GetTopCollectiblesResponse.parse_raw(b=api.call(json=request.dict()).content)

    def checkout_amount(self, c_id: str):
        api = CheckoutAmountApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = common.CheckoutAmountRequest(variables=common.CheckoutAmountRequest.Variables(id=c_id))
        return common.CheckoutAmountResponse.parse_raw(b=api.call(json=request.dict()).content)
