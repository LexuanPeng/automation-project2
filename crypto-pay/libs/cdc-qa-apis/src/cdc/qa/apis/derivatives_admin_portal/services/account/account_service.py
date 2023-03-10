import json
import logging

import urllib3

from ...models.account import AccountServiceMethodEnum, AccountSystemNameEnum
from ...models.admin import SHARD_NAMES
from ..admin import AdminBaseService

urllib3.disable_warnings()
logger = logging.getLogger(__name__)


class AccountService(AdminBaseService):
    def get_user_account_details(
        self,
        email: str = None,
        account: str = None,
        user: str = None,
        target_host_ip: str = AccountSystemNameEnum.ACCOUNT_SERVICE.value,
    ):
        """
        Get user account details by email
        @param account:
        @param user:
        @param email:
        @param target_host_ip: you can get the target_host_ip by get_target_host_ip(system_name)
        """
        arguments = {}
        if email is None and account is None and user is None:
            raise Exception("Not provided email, account and user when get account details")
        if email is not None:
            arguments["email"] = email
        if account is not None:
            arguments["account"] = account
        if user is not None:
            arguments["user"] = user
        if not target_host_ip:
            target_host_ip = AccountSystemNameEnum.ACCOUNT_SERVICE.value

        get_user_account_details = None
        for shard_name in SHARD_NAMES.accounts:
            try:
                get_user_account_details = self._admin(
                    shard_name=shard_name,
                    command=AccountServiceMethodEnum.getUserAccountDetails,
                    target=target_host_ip,
                    arguments=arguments,
                )
                result = get_user_account_details[0].result
                if result == "[]":
                    continue
                else:
                    json_result = json.loads(result)
                    if not json_result[0][1]:
                        continue
                break
            except Exception as e:
                logger.error(f"get user account details on shard:{shard_name} failed!")
                logger.error(str(e))
                continue
        return get_user_account_details

    def get_user_account_shard_name(self, account_uuid):
        netloc = self._get_netloc()
        if netloc.startswith("dpre"):
            return SHARD_NAMES.accounts[0]
        else:
            account_detail = self.get_user_account_details(account=account_uuid)
            return account_detail[0].host

    def get_user_account_id_by_email(self, email: str):
        user_account_details = self.get_user_account_details(email=email)[0].result
        details_list = json.loads(user_account_details)
        user_account_id = details_list[0][0]
        return user_account_id
