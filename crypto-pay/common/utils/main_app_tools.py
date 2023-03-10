import threading

from cdc.qa.apis.rails import RailsApi
from cdc.qa.apis.rails.models import encrypt_passcode
import requests
import logging
import urllib3
from cdc.qa.helpers import RailsConsoleHelper
from cdc.qa.integrations.otp import get_totp

logger = logging.getLogger(__name__)

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

lock = threading.Lock()


class MainAppTools:
    _main_app_host = "https://st.mona.co"

    @classmethod
    def get_quotation_id(cls, from_currency: str, token: str, payment_sdk_url: str, pay_type: str = "payments"):
        """
        @param pay_type: payments or merchant_subscriptions
        @param from_currency: the currency you pay
        @param payment_sdk_url: payment sdk url or qr_code
        @param token: app login token
        @return: quotation_id
        """
        headers = {"Authorization": f"Bearer {token}"}
        cls.verify_phone_and_passcode(token)
        if pay_type == "payments":
            data = {"from": from_currency, "payment_data": payment_sdk_url}
            url = f"{cls._main_app_host}/api/pay/{pay_type}/quotation/create"
        else:
            data = {"from_currency": from_currency, "subscription_data": payment_sdk_url}
            url = f"{cls._main_app_host}/api/pay/{pay_type}/payments/quotation/create"

        r = requests.post(url=url, data=data, headers=headers, verify=False)
        if r.status_code == 200:
            t = r.json()
            if t["ok"] is False:
                raise Exception(f"【Get quotation id failed】： {str(t)}")
            logger.info(f"【Get quotation id passed】：{str(t)}")
            return t["quotation"]["id"]
        else:
            raise Exception(f"【Get quotation id failed】： {r.text}")

    @classmethod
    def pay_payment(cls, from_currency: str, payment_sdk_url: str, token: str, passcode: str, seed_2fa: str = None):
        """
        @param from_currency: the currency you pay
        @param payment_sdk_url: payment sdk url
        @param token: token
        @param passcode: login passcode
        @param seed_2fa: seed_2fa
        @return: r
        """
        url = f"{cls._main_app_host}/api/pay/payments/create"
        cls.verify_phone_and_passcode(token, passcode=passcode)
        if seed_2fa is not None:
            # Scan the payment and input the 2fa code
            MainAppTools.pay_qr_code(token, payment_sdk_url, seed_2fa)

        quotation_id = MainAppTools.get_quotation_id(
            from_currency=from_currency, payment_sdk_url=payment_sdk_url, token=token
        )
        passcode = encrypt_passcode(passcode)

        headers = {"Authorization": f"Bearer {token}"}
        data = {"passcode": passcode, "payment_data": payment_sdk_url, "quotation_id": quotation_id}
        r = requests.post(url=url, json=data, headers=headers, verify=False)
        if r.status_code == 200:
            t = r.json()
            if t["ok"] is False:
                raise Exception(f"【Pay payment by main app failed】： {r.text}")
            logger.info(f"【Pay payment by main app passed】：{str(t)}")
            return t
        else:
            raise Exception(f"【Pay payment by main app failed】： {r.text}")

    @classmethod
    def activate_subscription(
        cls, subscriptions_id: str, sk_key: str, from_currency: str, token: str, passcode: str, apis
    ):
        """
        @param apis: apis
        @param subscriptions_id:  subscriptions_id
        @param sk_key:  secret key for shop
        @param from_currency:  pay by currency
        @param token: app token
        @param passcode:  passcode
        @return: r
        """
        url = f"{cls._main_app_host}/api/pay/merchant_subscriptions/activate"
        headers = {"Authorization": f"Bearer {token}"}

        subscriptions_details = apis.subscriptions.get_subscriptions(subscriptions_id, sk_key)
        qr_cde = subscriptions_details["qr_code"]
        quotation_id = MainAppTools.get_quotation_id(
            from_currency=from_currency, token=token, pay_type="merchant_subscriptions", payment_sdk_url=qr_cde
        )
        passcode = encrypt_passcode(passcode)
        data = {
            "passcode": passcode,
            "subscription_data": qr_cde,
            "quotation_id": quotation_id,
            "currency": from_currency,
        }

        r = requests.post(url=url, json=data, headers=headers, verify=False)
        if r.status_code == 200:
            t = r.json()
            if t["ok"] is False:
                raise Exception(f"【Activate the subscription by main app failed】： {str(t)}")
            logger.info(f"【Activate the subscription by main app passed】：{str(t)}")
            return t
        else:
            raise Exception(f"【Activate the subscription by main app failed】： {r.text}")

    @classmethod
    def get_transaction_record(cls, token: str, status: str = "all", count: str = "5"):
        """
        @param token: login token
        @param status: txn status
        @param count: txn records count
        @return: r: list
        """
        url = f"{cls._main_app_host}/api/crypto_pay/transactions"
        cls.verify_phone_and_passcode(token)
        headers = {"Authorization": f"Bearer {token}"}
        params = {"status": status, "count": count}
        r = requests.get(url=url, params=params, headers=headers, verify=False)

        if r.status_code == 200:
            t = r.json()
            if t["ok"] is False:
                raise Exception(f"【Get transaction from main app failed】： {str(t)}")
            logger.info(f"【Get transaction from main app passed】：{str(t)}")
            return t["transactions"]
        else:
            raise Exception(f"【Get transaction from main app failed】： {r.text}")

    @classmethod
    def get_user_details(cls, token: str):
        """
        @param token: login token
        @return: t["user"]
        """
        url = f"{cls._main_app_host}/api/user/show"
        headers = {"Authorization": f"Bearer {token}"}
        r = requests.get(url=url, headers=headers, verify=False)

        if r.status_code == 200:
            t = r.json()
            if t["ok"] is False:
                raise Exception(f"【Get user details from main app failed】： {str(t)}")
            logger.info(f"【Get user details from main app passed】：{str(t)}")
            return t["user"]
        else:
            raise Exception(f"【Get user details from main app failed】： {r.text}")

    @classmethod
    def get_user_config(cls, token: str):
        """
        @param token: login token
        @return: r
        """
        url = f"{cls._main_app_host}/api/user/configs"

        headers = {"Authorization": f"Bearer {token}"}
        r = requests.get(url=url, headers=headers, verify=False)

        if r.status_code == 200:
            t = r.json()
            if t["ok"] is False:
                raise Exception(f"【Get user config from main app failed】： {str(t)}")
            logger.info(f"【Get user config from main app passed】：{str(t)}")
            return t
        else:
            raise Exception(f"【Get user config from main app failed】： {r.text}")

    @classmethod
    def get_live_rates(cls, token, from_c: str, to_c: str, fixed_rate: str = "false"):
        """
        @param token: login token
        @param from_c: from currency
        @param to_c: to currency
        @param fixed_rate: fixed rate
        @return: r
        """
        url = f"{cls._main_app_host}/api/live_rates/tiers"
        cls.verify_phone_and_passcode(token)

        headers = {"Authorization": f"Bearer {token}"}
        params = {"from": from_c, "to": to_c, "fixed_rate": fixed_rate}

        r = requests.get(url=url, params=params, headers=headers, verify=False)
        if r.status_code == 200:
            t = r.json()
            if t["ok"] is False:
                raise Exception(f"【Get live rate from main app failed】： {str(t)}")
            logger.info(f"【Get live rate from main app passed】：{str(t)}")
            return t["live_rates"]
        else:
            raise Exception(f"【Get live rate from main app failed】： {r.text}")

    @classmethod
    def get_main_app_token(cls, rails_helper: RailsConsoleHelper, main_app_email: str):
        with lock:
            try:
                # rails_console_helper = RailsConsoleHelper()
                rails_api = RailsApi()
                magic_token = rails_helper.get_magic_token(main_app_email)
                token = rails_api.auth.authenticate(main_app_email, magic_token)
                logger.info(f"【Get main app token from email {main_app_email}】: {token}")
                return token
            except Exception as e:
                logger.error(f"【Get main app token from email {main_app_email} failed】: {str(e)}")
        return None

    @classmethod
    def update_pay_merchant_refund_currency(cls, token: str, refund_currency: str):
        headers = {"AUTHORIZATION": f"Bearer {token}"}
        cls.verify_phone_and_passcode(token=token)
        url = f"{cls._main_app_host}/api/user/configs/pay_merchant_refund_currency/update"
        data = {"pay_merchant_refund_currency": refund_currency}

        r = requests.post(url=url, data=data, headers=headers)
        if r.status_code == 200:
            t = r.json()
            if t["ok"] is False:
                raise Exception(f"【Update the main app user pay merchant refund currency failed】： {str(t)}")
            logger.info(f"【Update the main app user pay merchant refund currency passed】：{str(t)}")
            return t
        else:
            raise Exception(f"【Update the main app user pay merchant refund currency failed】： {r.text}")

    @classmethod
    def pay_qr_code(cls, token: str, qr_code_content: str, seed_2fa: str = None):
        headers = {"AUTHORIZATION": f"Bearer {token}"}
        url = f"{cls._main_app_host}/api/pay/qr_code/scan"
        cls.verify_phone_and_passcode(token=token)
        data = {"qr_code_content": qr_code_content}
        r = requests.post(url=url, headers=headers, json=data)

        if seed_2fa is not None:
            for i in range(0, 10):
                otp = get_totp(seed_2fa)
                data["otp"] = otp
                r = requests.post(url=url, headers=headers, json=data)
                t = r.json()
                if t["ok"] is False:
                    continue
                else:
                    logger.info(f"【Verify 2fa code before pay passed】: {str(t)}")
                    return t
            raise Exception(f"【Verify 2fa code before pay passed】: {str(r.text)}")
        else:
            if r.status_code == 200:
                t = r.json()
                if t["ok"] is False:
                    raise Exception(f"【Pay or refund the merchant qr_code failed】： {str(t)}")
                logger.info(f"【Pay or refund the merchant qr_code passed】：{str(t)}")
                return t
            else:
                raise Exception(f"【Pay or refund the merchant qr_code failed】： {r.text}")

    @classmethod
    def update_subscriptions_wallet(cls, token: str, subscriptions_id: str, to_wallet_currency: str, passcode: str):
        headers = {"AUTHORIZATION": f"Bearer {token}"}
        url = f"{cls._main_app_host}/api/pay/merchant_subscriptions/{subscriptions_id}/currency"
        passcode = encrypt_passcode(passcode)
        data = {"passcode": passcode, "currency": to_wallet_currency}
        cls.verify_phone_and_passcode(token)

        r = requests.put(url=url, json=data, headers=headers)
        if r.status_code == 200:
            t = r.json()
            if t["ok"] is False:
                raise Exception(f"【Update subscriptions wallet {to_wallet_currency} failed】： {str(t)}")
            logger.info(f"【Update subscriptions wallet {to_wallet_currency} passed】：{str(t)}")
            return t
        else:
            raise Exception(f"【Update subscriptions wallet {to_wallet_currency} failed】： {r.text}")

    @classmethod
    def deactivate_subscriptions(cls, token: str, subscriptions_id: str, passcode: str):
        headers = {"AUTHORIZATION": f"Bearer {token}"}

        passcode = encrypt_passcode(passcode)
        cls.verify_phone_and_passcode(token)
        url = f"{cls._main_app_host}/api/pay/merchant_subscriptions/request_deactivation"
        data = {"passcode": passcode, "pay_subscription_id": subscriptions_id}

        r = requests.post(url=url, data=data, headers=headers)
        if r.status_code == 200:
            t = r.json()
            if t["ok"] is False:
                raise Exception(f"【Deactivate subscriptions {subscriptions_id} failed】： {str(t)}")
            logger.info(f"【Deactivate subscriptions {subscriptions_id} passed】：{str(t)}")
            return t
        else:
            raise Exception(f"【Deactivate subscriptions {subscriptions_id} failed】： {r.text}")

    @classmethod
    def get_subscriptions_by_id(
        cls, token: str, subscriptions_id: str, subs_type: str = "active_merchant_subscriptions"
    ):
        headers = {"AUTHORIZATION": f"Bearer {token}"}
        url = f"{cls._main_app_host}/api/pay/merchant_subscriptions"
        r = requests.get(url=url, headers=headers)
        if r.status_code == 200:
            t = r.json()
            if t["ok"] is False:
                raise Exception(f"【Get subscriptions by {subscriptions_id} failed】： {str(t)}")
            merchant_subscriptions: list = t[subs_type]
            exp_sub_details = list(
                filter(lambda x: x["pay_subscription_id"] == subscriptions_id, merchant_subscriptions)
            )
            if len(exp_sub_details) > 0:
                return exp_sub_details
            else:
                raise Exception(f"【Get subscriptions by {subscriptions_id} failed】： len(exp_sub_details) <= 0")
        else:
            raise Exception(f"【Get subscriptions by {subscriptions_id} failed】： {r.text}")

    @classmethod
    def get_total_balances(cls, token: str):
        headers = {"AUTHORIZATION": f"Bearer {token}"}
        url = f"{cls._main_app_host}/api/balances/total"
        r = requests.get(url=url, headers=headers)

        if r.status_code == 200:
            t = r.json()
            if t["ok"] is False:
                raise Exception(f"【Get total balances failed】： {str(t)}")
            balances: dict = r.json()["balances"]
            logger.info(f"【Get total balances passed】: {str(t)}")
            return balances
        else:
            logger.error(f"【Get total balances failed】： {str(r.text)}")
            raise Exception(f"【Get total balances failed】： {str(r.text)}")

    @classmethod
    def verify_phone_and_passcode(cls, token: str, number: str = "123456", passcode: str = "123456"):
        headers = {"AUTHORIZATION": f"Bearer {token}"}
        # Send otp
        send_otp_url = f"{cls._main_app_host}/api/user/phone/send_otp"
        send_otp_r = requests.post(url=send_otp_url, headers=headers, data={"domain": "login"})
        # Verify phone
        verify_otp_url = f"{cls._main_app_host}/api/user/phone/verify_otp"
        verify_opt_r = requests.post(url=verify_otp_url, headers=headers, data={"phone_otp": encrypt_passcode(number)})
        # Verify passcode
        verify_passcode_url = f"{cls._main_app_host}/api/user/passcode/verify"
        passcode_data = {"passcode": encrypt_passcode(passcode), "biometric": False}
        passcode_headers = {"Authorization": f"Bearer {token}"}
        verify_passcode_r = requests.post(url=verify_passcode_url, data=passcode_data, headers=passcode_headers)
        logger.info(f"Verify phone and passcode responses: {send_otp_r}\n{verify_opt_r}\n{verify_passcode_r}")

    @classmethod
    def get_main_app_currency_balance(cls, token: str, currency: str):
        headers = {"AUTHORIZATION": f"Bearer {token}"}
        url = f"{cls._main_app_host}/api/account/show"
        r = requests.get(url=url, headers=headers)

        if r.status_code == 200:
            t = r.json()
            if t["ok"] is False:
                raise Exception(f"【Get balance of {currency} failed】： {str(t)}")
            wallets: list = r.json()["account"]["wallets"]
            filtered_wallet = list(filter(lambda x: x["currency"] == currency, wallets))
            wallet_amount = filtered_wallet[0]["balance"]["amount"]
            logger.info(f"【Get balance of {currency} passed】: {str(wallet_amount)}")
            return wallet_amount
        else:
            logger.error(f"【Get balances of {currency} failed】： {str(r.text)}")
            raise Exception(f"【Get balances of {currency} failed】： {str(r.text)}")
