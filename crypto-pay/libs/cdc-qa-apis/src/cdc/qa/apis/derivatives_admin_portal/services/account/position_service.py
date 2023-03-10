import logging

import urllib3

from . import AccountService
from ...models.account import AccountSystemNameEnum, PositionServiceMethodEnum
from ..admin import AdminBaseService

urllib3.disable_warnings()
logger = logging.getLogger(__name__)


class PositionService(AdminBaseService):
    def user_transfer_to_wallet(
        self,
        account_id: str,
        instrument_name: str,
        qty_delta: str,
        cost_delta: str,
        target_host_ip: str = AccountSystemNameEnum.POSITION_SERVICE.value,
    ):
        """
        transfer to deriv
        @param account_id:
        @param instrument_name:
        @param qty_delta: need transfer coin, it can be negative and positive
        @param cost_delta: need transfer coin, it can be negative and positive
        @param target_host_ip: you can get the target_host_ip by get_target_host_ip(system_name)
        """
        if not target_host_ip:
            target_host_ip = AccountSystemNameEnum.POSITION_SERVICE.value
        instrument_id = self.get_instrument_id(instrument_symbol=instrument_name)
        journals = [
            {
                "account": account_id,
                "instrument": instrument_id,
                "qtyDelta": qty_delta,
                "costDelta": cost_delta,
            }
        ]
        arguments = {"journals": journals}
        account_service = AccountService(host=self.host)
        shard_name = account_service.get_user_account_shard_name(account_uuid=account_id)
        admin_result = self._admin(
            shard_name=shard_name,
            command=PositionServiceMethodEnum.applyJournal,
            target=target_host_ip,
            arguments=arguments,
        )
        for res in admin_result:
            if res.success:
                return True
        return False
