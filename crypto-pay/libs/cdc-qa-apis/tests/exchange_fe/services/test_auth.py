from .mock.auth import *  # noqa
from cdc.qa.apis.exchange_fe.services.auth import ExchangeAuthService
from pytest import fixture
import base64


@fixture(scope="session")
def init_exchange_auth_service():
    otp_secret = "otp_secret"
    otp_secret = base64.b32encode(s=otp_secret.encode("utf-8"))
    auth_service = ExchangeAuthService(
        user_email="user_email", user_password="user_password", otp_secret=otp_secret, client_id=1
    )
    return auth_service


def test_oauth_authorize_login_url(init_exchange_auth_service):
    expected = (
        "https://st.mona.co/oauth/authorize?client_id=1&redirect_uri=https%3A%2F%2Fxdev-www.3ona.co%2F"
        "fe-ex-api%2Foauth_redirect&response_type=code&scope=exapi&login_type=login"
    )
    actual = init_exchange_auth_service._get_oauth_authorize_url()
    assert actual == expected


def test_oauth_authorize_back_url(init_exchange_auth_service):
    expected = (
        "https://st.mona.co/oauth/authorize?client_id=1&redirect_uri=https%3A%2F%2Fxdev-www.3ona.co%2F"
        "fe-ex-api%2Foauth_redirect&response_type=code&scope=exapi"
    )
    actual = init_exchange_auth_service._get_oauth_authorize_url(for_login=False)
    assert actual == expected


def test_access_oauth_login(init_exchange_auth_service, mock_oauth_authorize_login):
    oauth_login_url = init_exchange_auth_service._get_oauth_authorize_url()
    sign_in_url = init_exchange_auth_service._access_oauth(oauth_login_url, for_login=True)
    assert sign_in_url == "https://st.mona.co/users/sign_in"


def test_access_oauth(init_exchange_auth_service, mock_oauth_authorize):
    oauth_back_url = init_exchange_auth_service._get_oauth_authorize_url(for_login=False)
    access_token_url = init_exchange_auth_service._access_oauth(oauth_back_url, for_login=False)
    assert access_token_url == "https://xdev-www.3ona.co/fe-ex-api/oauth_redirect?code=1"


def test_get_csrf_token(init_exchange_auth_service, mock_get_sign_in_url):
    csrf_token = init_exchange_auth_service._get_csrf_token("https://st.mona.co/users/sign_in")
    assert csrf_token == "2"


def test_sign_in_and_redirect_otp_verify_url(
    init_exchange_auth_service, mock_sign_in_and_redirect_to_otp_verify_url, mock_get_sign_in_url
):
    init_exchange_auth_service._sign_in()
    assert init_exchange_auth_service.is_otp_verify


def test_sign_in_and_redirect_oauth_authorize(
    init_exchange_auth_service, mock_sign_in_and_redirect_to_oauth_authorize_url, mock_get_sign_in_url
):
    init_exchange_auth_service._sign_in()
    assert not init_exchange_auth_service.is_otp_verify


def test_otp_verify_and_redirect_oauth_authorize(
    init_exchange_auth_service, mock_otp_verify_and_redirect_to_oauth_authorize_url, mock_get_otp_verify_url
):
    oauth_authorize_url = init_exchange_auth_service._get_oauth_authorize_url(for_login=False)
    url = init_exchange_auth_service._otp_verify()
    assert url == oauth_authorize_url


def test_get_token(init_exchange_auth_service, mock_generate_exchange_token):
    access_token_url = "https://xdev-www.3ona.co/fe-ex-api/oauth_redirect?code=1"
    init_exchange_auth_service._access_token_url(access_token_url)
    assert init_exchange_auth_service.get_exchange_token() == "3"
