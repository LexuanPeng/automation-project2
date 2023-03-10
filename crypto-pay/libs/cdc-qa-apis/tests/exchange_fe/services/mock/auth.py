from pytest import fixture


@fixture()
def mock_oauth_authorize_login(requests_mock):
    requests_mock.get(
        "https://st.mona.co/oauth/authorize?client_id=1"
        "&login_type=login&redirect_uri=https%3A%2F%2Fxdev-www.3ona.co%2Ffe-ex-api%2Foauth_redirect&response_type=code"
        "&scope=exapi",
        status_code=302,
        headers={"location": "https://st.mona.co/users/sign_in"},
    )


@fixture()
def mock_oauth_authorize(requests_mock):
    requests_mock.get(
        "https://st.mona.co/oauth/authorize?client_id=1"
        "&redirect_uri=https%3A%2F%2Fxdev-www.3ona.co%2Ffe-ex-api%2Foauth_redirect&response_type=code"
        "&scope=exapi",
        status_code=302,
        headers={"location": "https://xdev-www.3ona.co/fe-ex-api/oauth_redirect?code=1"},
    )


@fixture()
def mock_get_sign_in_url(requests_mock):
    requests_mock.get(
        "https://st.mona.co/users/sign_in",
        text='<title>Crypto.com OAuth</title><meta name="csrf-param" content="authenticity_token" />'
        '<meta name="csrf-token" content="2" />',
        status_code=200,
    )


@fixture()
def mock_sign_in_and_redirect_to_otp_verify_url(requests_mock):
    requests_mock.post(
        "https://st.mona.co/users/sign_in",
        status_code=302,
        headers={"location": "https://st.mona.co/users/totp/verify"},
    )


@fixture()
def mock_get_otp_verify_url(requests_mock):
    requests_mock.get(
        "https://st.mona.co/users/totp/verify",
        text='<meta name="csrf-token" content="2" />',
        status_code=200,
    )


@fixture()
def mock_otp_verify_and_redirect_to_oauth_authorize_url(requests_mock):
    requests_mock.post(
        "https://st.mona.co/users/totp/verify",
        status_code=302,
        headers={
            "location": "https://st.mona.co/oauth/authorize?client_id=1&redirect_uri=https%3A%2F%2Fxdev-www.3ona.co%2F"
            "fe-ex-api%2Foauth_redirect&response_type=code&scope=exapi"
        },
    )


@fixture()
def mock_sign_in_and_redirect_to_oauth_authorize_url(requests_mock):
    requests_mock.post(
        "https://st.mona.co/users/sign_in",
        status_code=302,
        headers={
            "location": "https://st.mona.co/oauth/authorize?client_id=1"
            "&redirect_uri=https%3A%2F%2Fxdev-www.3ona.co%2Ffe-ex-api%2Foauth_redirect"
            "&response_type=code&scope=exapi"
        },
    )


@fixture()
def mock_generate_exchange_token(requests_mock):
    requests_mock.get(
        "https://xdev-www.3ona.co/fe-ex-api/oauth_redirect?code=1",
        status_code=302,
        headers={
            "location": "https://xdev-www.3ona.co/exchange",
            "set-cookie": "token=3; secure; " "SameSite=lax; Domain=3ona.co; Path=/",
        },
    )
