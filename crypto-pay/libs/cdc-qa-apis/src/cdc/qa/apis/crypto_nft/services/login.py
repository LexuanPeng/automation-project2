from cdc.qa.apis.crypto_nft.models import NFTRestApi, NFTClientService, auth
from .tools import compare_dict


class AuthByEmailApi(NFTRestApi):
    response_type = auth.AuthenticateByEmailResponse


class AuthenticateApi(NFTRestApi):
    response_type = auth.AuthenticateResponse


class PrepareEmailOtpApi(NFTRestApi):
    response_type = auth.PrepareEmailOtpResponse


class ContinuationOtpApi(NFTRestApi):
    response_type = auth.ContinueAuthResponse


class AuthenticateWithOtpApi(NFTRestApi):
    response_type = auth.AuthenticateWithOtpResponse


class RequestQrCodeLoginApi(NFTRestApi):
    response_type = auth.RequestQrCodeLoginResponse


class GetQrCodeLoginStatusApi(NFTRestApi):
    response_type = auth.GetQrCodeLoginStatusResponse


class AuthenticateByQrCodeApi(NFTRestApi):
    response_type = auth.AuthenticateByQrCodeResponse


class SendSmsCodeApi(NFTRestApi):
    response_type = auth.SendSmsCodeResponse


class RequestResetPasswordApi(NFTRestApi):
    response_type = auth.RequestResetPasswordResponse


class LogoutApi(NFTRestApi):
    response_type = auth.LogoutResponse


class RefreshTokenApi(NFTRestApi):
    response_type = auth.RefreshTokenResponse


class LoginService(NFTClientService):
    def auth_by_email(self, email: str, password: str) -> auth.AuthenticateByEmailResponse:
        api = AuthByEmailApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = auth.AuthenticateByEmailRequest(
            variables=auth.AuthenticateByEmailRequest.Variables(email=email, password=password, recaptcha={})
        )
        return auth.AuthenticateByEmailResponse.parse_raw(b=api.call(json=request.dict()).content)

    def authenticate(self, email: str, password: str) -> auth.AuthenticateResponse:
        api = AuthenticateApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = auth.AuthenticateRequest(
            variables=auth.AuthenticateRequest.Variables(email=email, password=password, recaptcha={})
        )
        return auth.AuthenticateResponse.parse_raw(b=api.call(json=request.dict()).content)

    def prepare_otp(self, token: str = None) -> auth.PrepareEmailOtpResponse:
        api = PrepareEmailOtpApi(host=self.host, _session=self.session, nft_token=token)
        request = auth.PrepareEmailOtpRequest()
        return auth.PrepareEmailOtpResponse.parse_raw(b=api.call(json=request.dict()).content)

    def continue_auth(self, otp_code: dict, token: str = None) -> auth.ContinueAuthResponse:
        api = ContinuationOtpApi(host=self.host, _session=self.session, nft_token=token)
        request = auth.ContinueAuthRequest(variables=auth.ContinueAuthRequest.Variables(**otp_code)).dict()
        request = compare_dict(otp_code, request)
        return auth.ContinueAuthResponse.parse_raw(b=api.call(json=request).content)

    def auth_with_otp(self, otp_code: dict, token: str = None) -> auth.AuthenticateWithOtpResponse:
        api = AuthenticateWithOtpApi(host=self.host, _session=self.session, nft_token=token)
        request = auth.AuthenticateWithOtpRequest(variables=auth.AuthenticateWithOtpRequest.Variables(**otp_code))
        return auth.AuthenticateWithOtpResponse.parse_raw(b=api.call(json=request.dict()).content)

    def request_qrcode_login(self, ott: str) -> auth.RequestQrCodeLoginResponse:
        api = RequestQrCodeLoginApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = auth.RequestQrCodeLoginRequest(variables=auth.RequestQrCodeLoginRequest.Variables(ott=ott))
        return auth.RequestQrCodeLoginResponse.parse_raw(b=api.call(json=request.dict()).content)

    def get_qrcode_login_status(self) -> auth.GetQrCodeLoginStatusResponse:
        api = GetQrCodeLoginStatusApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = auth.GetQrCodeLoginStatusRequest()
        return auth.GetQrCodeLoginStatusResponse.parse_raw(b=api.call(json=request.dict()).content)

    def authenticate_by_qrcode(self, token: str) -> auth.AuthenticateByQrCodeResponse:
        api = AuthenticateByQrCodeApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = auth.AuthenticateByQrCodeRequest(
            variables=auth.AuthenticateByQrCodeRequest.Variables(
                recaptcha=auth.AuthenticateByQrCodeRequest.Variables.Recaptcha(token=token)
            )
        )
        return auth.AuthenticateByQrCodeResponse.parse_raw(b=api.call(json=request.dict()).content)

    def logout(self) -> auth.LogoutResponse:
        api = LogoutApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = auth.LogoutRequest()
        return auth.LogoutResponse.parse_raw(b=api.call(json=request.dict()).content)

    def send_sms_code(self, number: str, token: str = None) -> auth.SendSmsCodeResponse:
        api = SendSmsCodeApi(host=self.host, _session=self.session, nft_token=token)
        request = auth.SendSmsCodeRequest(variables=auth.SendSmsCodeRequest.Variables(phoneNumber=number, recaptcha={}))
        return auth.SendSmsCodeResponse.parse_raw(b=api.call(json=request.dict()).content)

    def request_reset_password(self, email: str) -> auth.RequestResetPasswordResponse:
        api = RequestResetPasswordApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = auth.RequestResetPasswordRequest(
            variables=auth.RequestResetPasswordRequest.Variables(email=email, recaptcha={})
        )
        return auth.RequestResetPasswordResponse.parse_raw(b=api.call(json=request.dict()).content)

    def refresh_token(self) -> auth.RefreshTokenResponse:
        api = RefreshTokenApi(host=self.host, _session=self.session, nft_token=self.nft_token)
        request = auth.RefreshTokenRequest()
        return auth.RefreshTokenResponse.parse_raw(b=api.call(json=request.dict()).content)
