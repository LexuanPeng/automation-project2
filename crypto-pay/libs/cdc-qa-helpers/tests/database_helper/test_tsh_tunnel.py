import pytest
from cdc.qa.helpers.database_helper.tsh_tunnel import TeleportTunnel
from cdc.qa.core import secretsmanager as sm


@pytest.fixture(scope="module")
def tsh_db_info() -> dict:
    envs_key = "exchange-db-info"
    tsh_db_info = sm.get_secret_json(envs_key)["TSH_DB"]
    return tsh_db_info


@pytest.fixture(scope="module")
def tunnel(tsh_db_info: dict):
    tsh_proxy = tsh_db_info["tsh_proxy"]
    tsh_port = tsh_db_info["tsh_port"]
    tsh_username = tsh_db_info["tsh_username"]
    tsh_password = tsh_db_info["tsh_password"]
    tsh_otp_secret = tsh_db_info["tsh_otp_secret"]
    tex_database_info = tsh_db_info["DATABASE_INFO"]["TEXDB"]
    env_db_info = tex_database_info["XDEV4"]
    db_identifier = env_db_info["database_identifier"]
    db_name = env_db_info["database_name"]
    db_username = env_db_info["database_user"]
    tunnel = TeleportTunnel(
        host=tsh_proxy,
        port=tsh_port,
        username=tsh_username,
        password=tsh_password,
        otp_secret=tsh_otp_secret,
        db_identifier=db_identifier,
        db_name=db_name,
        db_username=db_username,
    )
    return tunnel


@pytest.mark.slow
def test_tsh_login(tunnel: TeleportTunnel):
    tunnel.login()


@pytest.mark.slow
def test_tsh_is_login(tunnel: TeleportTunnel):
    assert tunnel.is_logged_in()


@pytest.mark.slow
def test_tsh_db_login(tunnel: TeleportTunnel):
    tunnel.db_login()


@pytest.mark.slow
def test_tsh_db_connect(tunnel: TeleportTunnel):
    tunnel.db_connect()


@pytest.mark.slow
def test_tsh_get_ssl_cert(tunnel: TeleportTunnel):
    sslrootcert, sslcert, sslkey = tunnel.get_ssl_cert_info()
    assert sslrootcert
    assert sslcert
    assert sslkey
