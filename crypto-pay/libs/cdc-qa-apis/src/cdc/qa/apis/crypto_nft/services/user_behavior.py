from cdc.qa.apis.crypto_nft.models import NFTRestApi, NFTClientService, user_behavior


class CreatePriceAlertApi(NFTRestApi):
    response_type = user_behavior.CreatePriceAlertResponse


class GetPriceAlertsApi(NFTRestApi):
    response_type = user_behavior.GetPriceAlertsResponse


class GetPriceAlertCountsApi(NFTRestApi):
    response_type = user_behavior.GetPriceAlertCountsResponse


class DeletePriceAlertApi(NFTRestApi):
    response_type = user_behavior.DeletePriceAlertResponse


class UserBehaviorService(NFTClientService):
    def create_price_alert(self, input: dict, token: str = None) -> user_behavior.CreatePriceAlertResponse:
        api = CreatePriceAlertApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = user_behavior.CreatePriceAlertRequest(
            variables=user_behavior.CreatePriceAlertRequest.Variables(input=input)
        )
        return user_behavior.CreatePriceAlertResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_price_alerts(
        self, target: str, first: int, skip: str, token: str = None
    ) -> user_behavior.GetPriceAlertsResponse:
        api = GetPriceAlertsApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = user_behavior.GetPriceAlertsRequest(
            variables=user_behavior.GetPriceAlertsRequest.Variables(target=target, first=first, skip=skip)
        )
        return user_behavior.GetPriceAlertsResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_price_alert_counts(self, token: str = None) -> user_behavior.GetPriceAlertCountsResponse:
        api = GetPriceAlertCountsApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = user_behavior.GetPriceAlertCountsRequest()
        return user_behavior.GetPriceAlertCountsResponse.parse_raw(b=api.call(json=request.dict()).content)

    def delete_price_alert(self, id: str, token: str = None) -> user_behavior.DeletePriceAlertResponse:
        api = DeletePriceAlertApi(
            host=self.host, _session=self.session, nft_token=self.nft_token if (token is None) else token
        )
        request = user_behavior.DeletePriceAlertRequest(
            variables=user_behavior.DeletePriceAlertRequest.Variables(
                input=user_behavior.DeletePriceAlertRequest.Variables.Input(id=id)
            )
        )
        return user_behavior.DeletePriceAlertResponse.parse_raw(b=api.call(json=request.dict()).content)
