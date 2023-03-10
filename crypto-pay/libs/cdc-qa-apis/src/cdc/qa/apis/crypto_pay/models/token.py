from cdc.qa.apis.crypto_pay.models import FrozenBaseModel, GqlRequest, GqlResponse
from pydantic import Field
from cdc.qa.apis.crypto_pay import graphql


class CreateCaptchaRequest(GqlRequest):
    query: str = graphql.token.CREATE_CAPTCHA


class CreateCaptchaResponse(GqlResponse):
    class CreateCaptcha(FrozenBaseModel):
        class Captcha(FrozenBaseModel):
            fallback: bool = Field()
            challenge: str = Field()
            geetestId: str = Field()
            newCaptcha: str = Field()
            signature: str = Field()

        createCaptcha: Captcha = Field()

    data: CreateCaptcha = Field()


class CreateTokenRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        class Captcha(FrozenBaseModel):
            challenge: str = Field()
            signature: str = Field()
            code: str = Field(default="automation|jordan")

        email: str = Field()
        password: str = Field()
        captcha: Captcha = Field()

    query: str = graphql.token.CREATE_TOKEN
    variables: Variables = Field()


class CreateTokenResponse(GqlResponse):
    class CreateToken(FrozenBaseModel):
        class Token(FrozenBaseModel):
            token: str = Field()
            totp: bool = Field()
            __typename: str = Field()

        createToken: Token = Field()

    data: CreateToken = Field()
