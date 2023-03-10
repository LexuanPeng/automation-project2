from typing import Optional, Union, List
from pydantic import Field
from datetime import datetime

from cdc.qa.apis.crypto_nft import graphql
from cdc.qa.apis.crypto_nft.models import GqlRequest, GqlResponse, FrozenBaseModel
from .models import MeModel, UnauthorizedMeModel


class AuthenticateByEmailRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        class Recaptcha(FrozenBaseModel):
            type: str = Field(default="RECAPTCHA_V3", description="login type: RECAPTCHA_V2 or RECAPTCHA_V3")
            token: str = Field(default="", description="token")
            action: str = Field(default="LOGIN")

        email: str = Field(description="login email")
        password: str = Field(description="password")
        recaptcha: Recaptcha = Field()

    operationName: str = Field(default="authenticateByEmail")
    query: str = graphql.auth.authenicateByEmail
    variables: Variables = Field()


class AuthenticateByEmailResponse(GqlResponse):
    class authByEmail(FrozenBaseModel):
        class authResponse(FrozenBaseModel):
            lastLoginAt: Union[str, None] = Field(description="last login time")
            requiredSteps: list = Field()
            token: str = Field()
            __typename: str = Field()

            class UnauthorizedMe(FrozenBaseModel):
                email: str = Field()
                name: Union[str, None] = Field()
                username: str = Field()
                uuid: str = Field()
                __typename: str = Field()

            unauthorizedMe: UnauthorizedMe = Field()

        authenticateByEmail: authResponse = Field()

    data: authByEmail = Field()


class AuthenticateRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        class Recaptcha(FrozenBaseModel):
            type: str = Field(default="RECAPTCHA_V3")
            token: str = Field(default="")
            action: str = Field(default="LOGIN")

        email: str = Field()
        password: str = Field()
        recaptcha: Recaptcha = Field()

    operationName: str = Field(default="authenticate")
    query: str = graphql.auth.authenticate
    variables: Variables = Field()


class AuthenticateResponse(GqlResponse):
    class authByE(FrozenBaseModel):
        class authResponse(FrozenBaseModel):
            token: str = Field()
            __typename: str = Field()

            me: UnauthorizedMeModel = Field()

        authenticate: authResponse = Field()

    data: authByE = Field()


class PrepareEmailOtpRequest(GqlRequest):
    operationName: str = Field(default="prepareEmailOtp")
    query: str = graphql.auth.prepareEmailOtp


class PrepareEmailOtpResponse(GqlResponse):
    class prepareEmailOtp(FrozenBaseModel):
        class OtpResponse(FrozenBaseModel):
            success: bool = Field()
            __typename: str = Field()

        prepareOtp: OtpResponse = Field()

    data: prepareEmailOtp = Field()


class ContinueAuthRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        emailOtpCode: Optional[str] = Field(description="Email verification code")
        clientOtpCode: Optional[str] = Field(description="2FA verification code")
        smsOtpCode: Optional[str] = Field(description="SMS verification code")

    operationName: str = Field(default="continueAuthentication")
    query: str = graphql.auth.continueAuthentication
    variables: Variables = Field()


class ContinueAuthResponse(GqlResponse):
    class GoOnAuth(FrozenBaseModel):
        class continueAuthenticationResp(FrozenBaseModel):
            token: str = Field()
            __typename: str = Field()

            me: Optional[MeModel] = Field()
            unauthorizedMe: Optional[UnauthorizedMeModel] = Field()
            requiredSteps: Optional[List[str]] = Field()

        continueAuthentication: continueAuthenticationResp = Field()

    data: Optional[GoOnAuth] = None


class AuthenticateWithOtpRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        otpCode: Optional[str] = Field()
        clientOtpCode: Optional[str] = Field()

    operationName: str = Field(default="authenticateWithOtp")
    query: str = graphql.auth.authenticateWithOtp
    variables: Variables = Field()


class AuthenticateWithOtpResponse(GqlResponse):
    class GoOnAuth(FrozenBaseModel):
        class authenticationWithOtpResp(FrozenBaseModel):
            token: str = Field()
            lastLoginAt: datetime = Field()
            __typename: str = Field()

            me: MeModel = Field()

        authenticateWithOtp: authenticationWithOtpResp = Field()

    data: GoOnAuth = Field()


class RequestQrCodeLoginRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        ott: str = Field()

    operationName: str = Field(default="requestQrCodeLogin")
    query: str = graphql.auth.requestQrCodeLogin
    variables: Variables = Field()


class RequestQrCodeLoginResponse(GqlResponse):
    class RequestQrCodeLoginData(FrozenBaseModel):
        class RequestQrCodeLogin(FrozenBaseModel):
            encodedQr: str = Field()
            sessionId: str = Field()
            status: str = Field()
            __typename: str = Field()

        requestQrCodeLogin: RequestQrCodeLogin = Field()

    data: RequestQrCodeLoginData = Field()


class GetQrCodeLoginStatusRequest(GqlRequest):
    operationName: str = Field(default="getQrCodeLoginStatus")
    query: str = graphql.auth.getQrCodeLoginStatus


class GetQrCodeLoginStatusResponse(GqlResponse):
    class GetQrCodeLoginStatusData(FrozenBaseModel):
        class QrCodeLoginStatus(FrozenBaseModel):
            status: str = Field(description="Qr Code login status")
            __typename: str = Field()

        qrCodeLoginStatus: QrCodeLoginStatus = Field()

    data: GetQrCodeLoginStatusData = Field()


class AuthenticateByQrCodeRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        class Recaptcha(FrozenBaseModel):
            type: str = Field(default="RECAPTCHA_V3", description="Login type: RECAPTCHA_V2 or RECAPTCHA_V3")
            token: str = Field(description="Request qrcode token")
            action: str = Field(default="QR_CODE_LOGIN", description="Login action: QR_CODE_LOGIN")

        recaptcha: Recaptcha = Field()

    operationName: str = Field(default="authenticateByQrCode")
    query: str = graphql.auth.authenticateByQrCode
    variables: Variables = Field()


class AuthenticateByQrCodeResponse(GqlResponse):
    class AuthenticateByQrCodeData(FrozenBaseModel):
        class AuthenticateByQrCode(FrozenBaseModel):
            token: str = Field(description="Request qrcode token")
            __typename: str = Field()

            me: MeModel = Field()

        authenticateByQrCode: AuthenticateByQrCode = Field()

    data: AuthenticateByQrCodeData = Field()


class LogoutRequest(GqlRequest):
    operationName: str = Field(default="logout")
    query: str = graphql.auth.logout


class LogoutResponse(GqlResponse):
    class Data(FrozenBaseModel):
        logout: Union[dict, None] = Field()

    data: Data = Field()


class SendSmsCodeRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        class Recaptcha(FrozenBaseModel):
            type: str = Field(default="RECAPTCHA_V3")
            token: str = Field(default="")
            action: str = Field(default="VERIFY_SMS")

        phoneNumber: str = Field()
        recaptcha: Recaptcha = Field()

    operationName: str = Field(default="sendSmsCode")
    query: str = graphql.auth.sendSmsCode
    variables: Variables = Field()


class SendSmsCodeResponse(GqlResponse):
    class SendSmsCodeData(FrozenBaseModel):
        class SendSmsCode(FrozenBaseModel):
            maskedRecipientPhoneNumber: str = Field(description="Phone number with last two number like +XX XXXX XXXX4")
            __typename: str = Field()

        sendSmsCode: SendSmsCode = Field()

    data: Optional[SendSmsCodeData] = None


class RequestResetPasswordRequest(GqlRequest):
    class Variables(FrozenBaseModel):
        class Recaptcha(FrozenBaseModel):
            type: str = Field(default="RECAPTCHA_V3")
            token: str = Field(default="")
            action: str = Field(default="FORGOT_PASSWORD")

        email: str = Field()
        recaptcha: Recaptcha = Field()

    operationName: str = Field(default="requestResetPasswordV2")
    query: str = graphql.auth.requestResetPassword
    variables: Variables = Field()


class RequestResetPasswordResponse(GqlResponse):
    class RequestResetPasswordData(FrozenBaseModel):
        class RequestResetPassword(FrozenBaseModel):
            status: str = Field()
            __typename: str = Field()
            token: Optional[str] = Field()

        requestResetPasswordV2: RequestResetPassword = Field()

    data: Optional[RequestResetPasswordData] = None


class RefreshTokenRequest(GqlRequest):
    operationName: str = Field(default="refreshToken")
    query: str = graphql.auth.refreshToken


class RefreshTokenResponse(GqlResponse):
    class Data(FrozenBaseModel):
        class RefreshToken(FrozenBaseModel):
            token: str = Field()
            me: MeModel = Field()

        refreshToken: RefreshToken = Field()

    data: Data = Field()
