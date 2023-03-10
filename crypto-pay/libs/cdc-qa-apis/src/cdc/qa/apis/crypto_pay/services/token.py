from cdc.qa.apis.common.models.rest_api import HttpMethods
from cdc.qa.apis.crypto_pay.models import (
    PayRestApi,
    PayDashBoardService,
    token,
)


class CreateCaptchaApi(PayRestApi):
    method = HttpMethods.POST
    response_type = token.CreateCaptchaResponse


class CreateTokenApi(PayRestApi):
    method = HttpMethods.POST
    response_type = token.CreateTokenResponse


class TokenService(PayDashBoardService):
    def _create_captcha(self) -> token.CreateCaptchaResponse:
        api = CreateCaptchaApi(host=self.host, _session=self.session)
        request = token.CreateCaptchaRequest()

        return token.CreateCaptchaResponse.parse_raw(b=api.call(json=request.dict()).content)

    def create_token(self, user_name: str, password: str) -> token.CreateTokenResponse:
        api = CreateTokenApi(host=self.host, _session=self.session)
        r = self._create_captcha().data.createCaptcha

        request = token.CreateTokenRequest(
            variables=token.CreateTokenRequest.Variables(
                email=user_name,
                password=password,
                captcha=token.CreateTokenRequest.Variables.Captcha(challenge=r.challenge, signature=r.signature),
            )
        )

        return token.CreateTokenResponse.parse_raw(b=api.call(json=request.dict()).content)
