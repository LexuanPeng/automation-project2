from .tsh_tunnel import TeleportTunnel
from .database_helper import DatabaseHelper


class TSHDatabaseHelper(DatabaseHelper):
    """A database helper connected through TSH tunnel."""

    # tsh variables
    TSH_PROXY: str = "internal-exchange-tk-sec-stag-aws.teleport.cdcinternal.com"
    TSH_PORT: int = 443
    TSH_USERNAME: str
    TSH_PASSWORD: str
    TSH_OTP_SECRET: str
    TSH_DB_IDENTIFIER: str

    # database variables
    DB_DIALECT: str
    DB_NAME: str = ""
    DB_USERNAME: str

    @staticmethod
    def create_tunnel(
        host: str,
        port: int,
        *,
        username: str,
        password: str,
        otp_secret: str,
        db_identifier: str,
        db_name: str,
        db_username: str,
    ) -> TeleportTunnel:
        tunnel = TeleportTunnel(
            host=host,
            port=port,
            username=username,
            password=password,
            otp_secret=otp_secret,
            db_identifier=db_identifier,
            db_name=db_name,
            db_username=db_username,
        )
        return tunnel
