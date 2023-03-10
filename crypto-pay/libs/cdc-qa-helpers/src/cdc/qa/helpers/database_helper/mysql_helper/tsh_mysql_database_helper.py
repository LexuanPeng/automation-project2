from ..tsh_database_helper import TSHDatabaseHelper


class TSHMySQLDBHelper(TSHDatabaseHelper):
    # tsh variables
    TSH_LOCAL_BIND_PORT: int

    # database variables
    DB_DIALECT: str = "mysql+pymysql"

    def __init__(self):
        # open tsh tunnel
        tunnel = self.create_tunnel(
            host=self.TSH_PROXY,
            port=self.TSH_PORT,
            username=self.TSH_USERNAME,
            password=self.TSH_PASSWORD,
            otp_secret=self.TSH_OTP_SECRET,
            db_identifier=self.TSH_DB_IDENTIFIER,
            db_name=self.DB_NAME,
            db_username=self.DB_USERNAME,
        )
        tunnel.start()
        tunnel.as_proxy(local_bind_host="", local_bind_port=self.TSH_LOCAL_BIND_PORT)
        sslrootcert, sslcert, sslkey = tunnel.get_ssl_cert_info()

        # connect to database
        self.engine = self.create_engine(
            dialect=self.DB_DIALECT,
            host=tunnel.local_bind_host,
            port=tunnel.local_bind_port,
            username=self.DB_USERNAME,
            database=self.DB_NAME,
            connect_args={
                "ssl_ca": sslrootcert,
                "ssl_cert": sslcert,
                "ssl_key": sslkey,
            },
        )
