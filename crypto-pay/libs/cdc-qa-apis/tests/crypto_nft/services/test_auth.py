import pytest
from .mock.auth import *  # noqa
from cdc.qa.apis import crypto_nft as nft


@pytest.fixture
def auth_service():
    service = nft.GqlServices().login
    return service


def test_authenticate_by_email(auth_service, mock_authenticate_by_email):
    response = auth_service.auth_by_email(email="email@example.com", password="password")
    assert response.data.authenticateByEmail.token is not None
    assert isinstance(response.data.authenticateByEmail.requiredSteps, list)
    assert response.data.authenticateByEmail.unauthorizedMe.email == "example@crypto.com"
    assert response.data.authenticateByEmail.unauthorizedMe.name == "atr"
    assert response.data.authenticateByEmail.unauthorizedMe.username == "k6-example"
    assert response.data.authenticateByEmail.unauthorizedMe.uuid == "a99da057-29ae-46cd-bd6f-88ca68e09c6d"


def test_authenticate(auth_service, mock_authenticate):
    response = auth_service.authenticate(email="email@example.com", password="password")
    assert response.data.authenticate.token is not None
    assert response.data.authenticate.me.uuid == "a99da057-29ae-46cd-bd6f-88ca68e09c6d"
    assert response.data.authenticate.me.email == "k6-qiangfu@crypto.com"
    assert response.data.authenticate.me.clientOtpEnabled is False


def test_prepare_otp(auth_service, mock_prepare_otp):
    response = auth_service.prepare_otp()
    assert response.data.prepareOtp.success is True


def test_continue_authentication(auth_service, mock_continue_authentication):
    response = auth_service.continue_auth({"emailOtpCode": "12345678"})
    assert response.data.continueAuthentication.token is not None
    assert response.data.continueAuthentication.me.uuid == "a99da057-29ae-46cd-bd6f-88ca68e09c6d"
    assert response.data.continueAuthentication.me.id == "k6-qiangfu"
    assert response.data.continueAuthentication.me.mainAppStatus == "KYC_APPROVED"
    assert response.data.continueAuthentication.me.isCreationPayoutBlocked is False
    assert response.data.continueAuthentication.me.croUserUUID == "b3b7df95-7f2b-4447-b408-fe7d1fe00112"
    assert response.data.continueAuthentication.me.croWalletAddress == "tcro1k7hsy88nwl7k64yqk75nckq90plgk87r03dr2r"
    assert response.data.continueAuthentication.me.creatorConfig.canCreateAsset is True
    assert response.data.continueAuthentication.me.creatorConfig.maxAssetsPerWeek == 50
    assert response.data.continueAuthentication.me.weeklyUsedCreditCardBalanceDecimal.drops == "0.00"
    assert response.data.continueAuthentication.me.weeklyUsedCreditCardBalanceDecimal.marketplace == "0.00"


def test_auth_with_otp(auth_service, mock_auth_with_otp):
    response = auth_service.auth_with_otp(otp_code={"otpCode": "12345678"})
    assert response.data.authenticateWithOtp.token is not None
    assert response.data.authenticateWithOtp.me.uuid == "a99da057-29ae-46cd-bd6f-88ca68e09c6d"
    assert response.data.authenticateWithOtp.me.id == "k6-qiangfu"
    assert response.data.authenticateWithOtp.me.mainAppStatus == "NO_ACCOUNT"
    assert response.data.authenticateWithOtp.me.isCreationPayoutBlocked is False
    assert response.data.authenticateWithOtp.me.croUserUUID == "b3b7df95-7f2b-4447-b408-fe7d1fe00112"
    assert response.data.authenticateWithOtp.me.croWalletAddress == "tcro1k7hsy88nwl7k64yqk75nckq90plgk87r03dr2r"
    assert response.data.authenticateWithOtp.me.creatorConfig.canCreateAsset is True
    assert response.data.authenticateWithOtp.me.creatorConfig.maxAssetsPerWeek == 50
    assert response.data.authenticateWithOtp.me.weeklyUsedCreditCardBalanceDecimal.drops == "0.00"
    assert response.data.authenticateWithOtp.me.weeklyUsedCreditCardBalanceDecimal.marketplace == "0.00"


def test_request_qrcode_login(auth_service, mock_request_qrcode_login):
    response = auth_service.request_qrcode_login("ott")
    assert response.data.requestQrCodeLogin.encodedQr is not None
    assert response.data.requestQrCodeLogin.sessionId is not None
    assert response.data.requestQrCodeLogin.status == "PENDING"


def test_get_qrcode_login_status(auth_service, mock_get_qrcode_login_status):
    response = auth_service.get_qrcode_login_status()
    assert response.data.qrCodeLoginStatus.status == "PENDING"


def test_authenticate_by_qrcode(auth_service, mock_authenticate_by_qrcode):
    response = auth_service.authenticate_by_qrcode("token")
    assert response.data.authenticateByQrCode.token is not None
    assert response.data.authenticateByQrCode.me.uuid == "8d120e1c-74d1-4a94-90dd-4410784f4f4e"
    assert response.data.authenticateByQrCode.me.id == "atest"


def test_logout(auth_service, mock_logout):
    response = auth_service.logout()
    assert response.data.logout is None
