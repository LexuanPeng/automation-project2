import json
import logging

from ..admin import AdminBaseService, SHARD_NAMES
from ...models.global_model import GlobalSystemNameEnum, AuthServiceMethodEum
from ...models.exceptions import GetAccountShardInfoException

logger = logging.getLogger(__name__)


class AuthService(AdminBaseService):
    def get_account_shard_id(self, account_uuid: str, target_host_ip: str = GlobalSystemNameEnum.AUTH_SERVICE.value):
        arguments = {"account": account_uuid}
        try:
            account_info = self._admin(
                shard_name=SHARD_NAMES.global_shard,
                command=AuthServiceMethodEum.getAccountShardInfo,
                target=target_host_ip,
                arguments=arguments,
            )
            result = account_info[0].result
            account_shard_result = json.loads(result)[0]
            seq_shard_id = account_shard_result[3]
            return seq_shard_id
        except Exception as e:
            logger.error("get account shard info failed!")
            logger.error(str(e))
            raise GetAccountShardInfoException("Get account shard info failed!")

    def get_account_shard_name_by_id(self, account_shard_id: int):
        netloc = self._get_netloc()
        if netloc.startswith("dpre"):
            return SHARD_NAMES.accounts[0]
        else:
            account_index = account_shard_id // 86
            return SHARD_NAMES.accounts[account_index]
