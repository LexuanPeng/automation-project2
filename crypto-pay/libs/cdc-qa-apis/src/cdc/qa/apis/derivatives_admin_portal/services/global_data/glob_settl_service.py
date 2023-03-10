import logging

from ..admin import AdminBaseService, SHARD_NAMES
from ...models.global_model import GlobalSystemNameEnum, GlobSettlServiceMethodEum

logger = logging.getLogger(__name__)


class GlobSettlService(AdminBaseService):
    def trigger_global_session_settlement(self, target_host_ip: str = GlobalSystemNameEnum.GLOB_SETTL_SERVICE.value):
        if not target_host_ip:
            target_host_ip = GlobalSystemNameEnum.GLOB_SETTL_SERVICE.value
        trigger_response = self._admin(
            shard_name=SHARD_NAMES.global_shard,
            command=GlobSettlServiceMethodEum.triggerGlobalSessionSettlement,
            target=target_host_ip,
            arguments={},
        )
        for each_result in trigger_response:
            try:
                if not each_result.success:
                    logger.warning(f"trigger global session settlement failed, target host ip is {each_result.host}")
                    return False
            except IndexError:
                return False
            except KeyError:
                return False
            except Exception as e:
                logger.error("trigger global session settlement failed!")
                logger.error(str(e))
                return False
        return True
