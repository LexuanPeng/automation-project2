from .tsh_mysql_database_helper import TSHMySQLDBHelper

from enum import Enum
from cdc.qa.core import secretsmanager as sm

DB_KEYWORDS_BLACKLIST: list = [
    "delete",
    "drop",
    "alter",
    "insert",
    "create",
]


class ExchangeMysqlHelper(TSHMySQLDBHelper):
    class ENV(Enum):
        XDEV = "XDEV"
        XSTA = "XSTA"
        XDEV4 = "XDEV4"
        XSTA2 = "XSTA2"

    def __init__(self, env: ENV):
        secret_id = "exchange-db-info"

        tsh_db_info = sm.get_secret_json(secret_id)["TSH_DB"]
        self.TSH_PROXY = tsh_db_info["tsh_proxy"]
        self.TSH_PORT = int(tsh_db_info["tsh_port"])
        self.TSH_USERNAME = tsh_db_info["tsh_username"]
        self.TSH_PASSWORD = tsh_db_info["tsh_password"]
        self.TSH_OTP_SECRET = tsh_db_info["tsh_otp_secret"]
        cu_database_info = tsh_db_info["DATABASE_INFO"]["CU"]
        env_db_info = cu_database_info[env.value]
        self.TSH_DB_IDENTIFIER = env_db_info["database_identifier"]
        self.TSH_LOCAL_BIND_PORT = int(env_db_info["custom_port"])

        # database variables
        self.DB_NAME = env_db_info["database_name"]
        self.DB_USERNAME = env_db_info["database_user"]

        super().__init__()

    def get_db_version(self) -> str:
        with self.engine.connect() as connection:
            sql = "SELECT VERSION();"
            result = connection.execute(sql)
            return next(result)[0]

    # ! It is not a good practice to allow executing arbitrary SQL queries freely.
    # * Consider writing specific methods with prepared query instead.
    def execute_sql(self, sql: str) -> list:
        """Execute a single SQL query.

        Args:
            sql (str): the SQL query to be executed.

        Raises:
            Exception: when the SQL query contains blacklisted keywords.

        Returns:
            list: the result from execution.
        """
        for keyword in DB_KEYWORDS_BLACKLIST:
            if keyword in sql.lower():
                # TODO: convert to specific exception
                raise Exception(f"Blacklisted keyword '{keyword}' found in SQL query: {sql}")

        with self.engine.connect() as connection:
            result = connection.execute(sql)
            if result.rowcount > 0:
                return [row._mapping.items() for row in result]
            else:
                return []
