import logging
from enum import Enum
from typing import Optional

from cdc.qa.core import secretsmanager as sm
from sqlalchemy.sql import text
import textwrap
from ..tsh_postgres_database_helper import TSHPostgresDatabaseHelper
from .models.account import AccountDetail
from .models.currency import CurrencyDetail
from .models.instrument_currency_market import InstrumentCurrencyMarketDetail
from .models.margin_loan_config import MarginLoanConfigDetail
from .models.sys_config import SysConfigDetail
from .models.domain_user import DomainUserDetail
from .models.vip_tier_rate import VIPTierRateDetail

logger = logging.getLogger(__name__)
DB_KEYWORDS_BLACKLIST: list = [
    "delete",
    "drop",
    "alter",
    "insert",
    "create",
]


class ExchangeTexdbHelper(TSHPostgresDatabaseHelper):
    """
    exchange-db-info TSH DB AWS SecretManager Demo:
    {
        "TSH_DB":{
            "tsh_otp_secret":"",
            "tsh_password":"",
            "tsh_port":"443",
            "tsh_proxy":"",
            "tsh_username":"",
            "DATABASE_INFO":{
                "TEXDB":{
                    "XDEV4":{
                        "database_identifier":"",
                        "database_name":"",
                        "database_user":""
                    }
                },
                "CU":{
                    "XDEV":{
                        "database_identifier":"",
                        "database_name":"",
                        "database_user":"",
                        "custom_port": ""
                    }
                }
            }
        }
    }
    """

    class ENV(Enum):
        XDEV = "XDEV"
        XSTA = "XSTA"
        XDEV4 = "XDEV4"
        XSTA2 = "XSTA2"

    def __init__(self, env: ENV):
        secret_id = "exchange-db-info"

        # tsh variables
        tsh_db_info = sm.get_secret_json(secret_id)["TSH_DB"]
        self.TSH_PROXY = tsh_db_info["tsh_proxy"]
        self.TSH_PORT = int(tsh_db_info["tsh_port"])
        self.TSH_USERNAME = tsh_db_info["tsh_username"]
        self.TSH_PASSWORD = tsh_db_info["tsh_password"]
        self.TSH_OTP_SECRET = tsh_db_info["tsh_otp_secret"]
        tex_database_info = tsh_db_info["DATABASE_INFO"]["TEXDB"]
        env_db_info = tex_database_info[env.value]
        self.TSH_DB_IDENTIFIER = env_db_info["database_identifier"]

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
    def execute_sql(self, sql: str, params: Optional[dict] = None) -> list:
        """Execute a single SQL query.

        Args:
            sql (str): the SQL query to be executed.

        Raises:
            Exception: when the SQL query contains blacklisted keywords.

        Returns:
            list: the result from execution.
        """
        logger.info(f"executing sql:{' '.join(textwrap.dedent(sql).splitlines())}, params:{params}")
        for keyword in DB_KEYWORDS_BLACKLIST:
            if keyword in sql.lower():
                # TODO: convert to specific exception
                raise Exception(f"Blacklisted keyword '{keyword}' found in SQL query: {sql}")

        with self.engine.connect() as connection:
            result = connection.execute(text(sql), params).fetchall()
            if len(result) > 0:  # .rowcount > 0:
                return [{column: value for column, value in row._mapping.items()} for row in result]  # type: ignore
            else:
                return []

    def get_account_info_by_email(self, email: str) -> AccountDetail:
        """get user fee discount by email

        Args:
            email (str): user email

        Returns:
            AccountDetail: account info
        """
        sql = """
            SELECT uuid, maker_fee_discount, taker_fee_discount FROM account
            WHERE product_type = 'SPOT' AND system_type = 'USER' AND master_account_uuid IS null AND uuid IN
            (SELECT uuid FROM domain_user WHERE email = :email);
            """
        account_list = self.execute_sql(sql, dict(email=email))
        if account_list:
            return AccountDetail.parse_obj(account_list[0])

        raise ValueError("AccountDetail not found.")

    def get_instrument_currency_market_by_name(self, instrument_name: str) -> InstrumentCurrencyMarketDetail:
        """get instrument fee rate

        Args:
            instrument_name (str): instrument name, e.g: BTC_USDT

        Returns:
            InstrumentCurrencyMarketDetail: data
        """
        sql = """
            SELECT symbol,
            base_currency,
            description,
            instrument_id,
            is_tradable,
            is_visible,
            maker_fee10th_bps,
            max_price,
            max_quantity,
            min_maker_fee10th_bps,
            min_price,
            min_quantity,
            min_taker_fee10th_bps,
            price_decimals,
            product_type,
            quantity_decimals,
            quote_currency,
            taker_fee10th_bps,
            cu_symbol,
            trading_group,
            margin_enabled,
            margin_enabled_5x,
            margin_enabled_10x,
            released_time,
            has_index_price
            FROM instrument_currency_market WHERE symbol = :instrument_name;
            """
        instruments = self.execute_sql(sql, dict(instrument_name=instrument_name))
        if instruments:
            return InstrumentCurrencyMarketDetail.parse_obj(instruments[0])

        raise ValueError("InstrumentCurrencyMarketDetail not found.")

    def get_sys_config_by_key(self, key_name: str) -> SysConfigDetail:
        """get system config

        Args:
            key_name (str): key name.

        Returns:
            SysConfigDetail: config data
        """
        sql = """
            SELECT key, value FROM public.sys_config WHERE key=:key_name;
            """
        key_list = self.execute_sql(sql, dict(key_name=key_name))
        if key_list:
            return SysConfigDetail.parse_obj(key_list[0])

        raise ValueError("SysConfigDetail not found.")

    def get_margin_loan_config_by_symbol_stake_amount(self, symbol: str, stake_amount: int) -> MarginLoanConfigDetail:
        """get margin loan config

        Args:
            symbol (str): symbol name, e.g:DOGE.
            stake_amount (int): stake amount, e.g:500000.

        Returns:
            MarginLoanConfigDetail: config data
        """
        sql = """
            SELECT stake_amount, symbol, hourly_rate, max_borrow_limit, min_borrow_limit, max_borrow_limit_5x,
            max_borrow_limit_10x FROM public.margin_loan_config
            WHERE symbol=:symbol AND stake_amount=:stake_amount;
            """

        config_list = self.execute_sql(sql, dict(symbol=symbol, stake_amount=stake_amount))
        if config_list:
            return MarginLoanConfigDetail.parse_obj(config_list[0])

        raise ValueError("MarginLoanConfigDetail not found.")

    def get_currency_info_by_name(self, symbol: str) -> CurrencyDetail:
        """get currency info

        Args:
            symbol (str): currency name

        Returns:
            CurrencyDetail: currency info data
        """
        sql = """
            SELECT symbol, decimals, display_decimals, is_tradable, is_stable_coin,
            daily_quantity_limit, daily_notional_limit
            FROM currency WHERE symbol=:symbol;
            """
        currency_list = self.execute_sql(sql, dict(symbol=symbol))
        if currency_list:
            return CurrencyDetail.parse_obj(currency_list[0])

        raise ValueError("CurrencyDetail not found.")

    def get_domain_user_info_by_email(self, email: str) -> DomainUserDetail:
        """
        Get domain user info
        Args:
            email (str): email

        Returns:
            DomainUserDetail
        """
        sql = """
            SELECT uuid,
            email,
            is_enabled,
            maker_fee_discount,
            taker_fee_discount,
            user_type,
            two_fa_enabled,
            two_fa_key,
            vip_tier,
            margin_access,
            mobile_number,
            derivatives_access,
            lending_access,
            is_lending_vip,
            deriv_maker_rate_bps,
            deriv_taker_rate_bps,
            deriv_vip_tier,
            effective_vip_tier,
            vip_tier_custom,
            spot_maker_fee_discount_custom,
            spot_taker_fee_discount_custom,
            deriv_maker_rate_bps_custom,
            deriv_taker_rate_bps_custom
            FROM domain_user WHERE email=:email;
            """
        domain_user_list = self.execute_sql(sql, dict(email=email))
        if domain_user_list:
            return DomainUserDetail.parse_obj(domain_user_list[0])

        raise ValueError("DomainUserDetail not found.")

    def get_vip_tier_info_by_vip_tier(self, vip_tier: int) -> VIPTierRateDetail:
        """
        Get domain user info
        Args:
            vip_tier (str): email

        Returns:
            VIPTierRateDetail
        """
        sql = """
        SELECT vip_tier,
        spot_maker_rate_pct,
        spot_taker_rate_pct,
        deriv_maker_rate_pct,
        deriv_taker_rate_pct
        FROM vip_tier_rate WHERE vip_tier=:vip_tier;
        """
        vip_tier_list = self.execute_sql(sql, dict(vip_tier=vip_tier))
        if vip_tier_list:
            return VIPTierRateDetail.parse_obj(vip_tier_list[0])

        raise ValueError("VIPTierRateDetail not found.")
