import json
import logging

import urllib3

from ...models.admin import SHARD_NAMES, AdminResponse
from ...models.exceptions import NotFoundException
from ...models.market_data import (
    MarketDataSystemNameEnum,
    ValuationNodeFieldEnum,
    ValuationNodeMethodEnum,
    ValuationNodeProfileEnum,
)
from ..admin import AdminBaseService

urllib3.disable_warnings()
logger = logging.getLogger(__name__)


class ValuationNodeService(AdminBaseService):
    def _get_valuation_value_from_response(
        self, valuation_resp: AdminResponse, field: ValuationNodeFieldEnum, index: int = 3
    ):
        try:
            result = valuation_resp[0].result
            list_result = json.loads(result)
            expected_r = []
            for each_item in list_result:
                if each_item[1] == field.value:
                    expected_r = each_item
                    return expected_r[index]
            else:
                raise NotFoundException(f"Failed to find the Field {field.value}")
        except Exception as e:
            logger.exception(e)
            raise Exception(f"get valuation value from resp failed! field:{field.value}")

    def set_valuation_override(
        self,
        instrument_id: str,
        field: ValuationNodeFieldEnum,
        is_override: str,
        profile: ValuationNodeProfileEnum = ValuationNodeProfileEnum.LIVE_EXCHANGE_OFFICIAL,
        value: str = None,
        target_host_ip: str = MarketDataSystemNameEnum.VALUATION_NODE.value,
    ) -> AdminResponse:
        """
        Set Valuation Override
        @param instrument_id: instrument id
        @param field: MARK_PRICE, INDEX_PRICE, FAIR_PRICE, FUNDING_RATE
        @param is_override: true/false
        @param profile: LIVE_EXCHANGE_OFFICIAL, LIVE_RISK_OFFICIAL, LIVE_TRADING_OFFICIAL, HOURLY_RISK_SMART_MARGIN,
        RESERVED_FOR_RISK_PORTFOLIO_MARGIN, RESERVED_FOR_RISK_PORTFOLIO_MARGIN_2
        @param value: string, the value for field
        @param target_host_ip: you can get the target_host_ip by get_target_host_ip(system_name)
        """
        if not target_host_ip:
            target_host_ip = MarketDataSystemNameEnum.VALUATION_NODE.value
        arguments = {
            "instrument": instrument_id,
            "field": field.value,
            "override": is_override,
            "profile": profile.value,
            "value": value,
        }

        set_valuation_result = None
        res_list = []
        # set valuation on each shard
        for shard_name in SHARD_NAMES.market_data:
            try:
                set_valuation_result = self._admin(
                    shard_name=shard_name,
                    command=ValuationNodeMethodEnum.setValuationOverride,
                    target=target_host_ip,
                    arguments=arguments,
                )
                res_list += set_valuation_result
            except Exception as e:
                logger.error(f"Set Valuation Override on shard:{shard_name} failed! error:{str(e)}")
                continue
        return res_list

    def get_valuation_result(self, instrument_id, target_host_ip: str = MarketDataSystemNameEnum.VALUATION_NODE.value):
        """
        Get valuation result by instrument id and target host ip
        """
        if not target_host_ip:
            target_host_ip = MarketDataSystemNameEnum.VALUATION_NODE.value
        arguments = {"instrument": instrument_id}
        for shard_name in SHARD_NAMES.market_data:
            try:
                get_valuation_result = self._admin(
                    shard_name=shard_name,
                    command=ValuationNodeMethodEnum.getValuationResult,
                    target=target_host_ip,
                    arguments=arguments,
                )
                if get_valuation_result[0].result == "[]":
                    continue
                break
            except Exception as e:
                logger.error(f"get valuation on shard:{shard_name} failed!")
                logger.error(str(e))
                continue
        return get_valuation_result

    def set_index_price(self, instrument_symbol: str, price_value: str = None, is_override: str = "true"):
        """set instrument index price

        Args:
            instrument_symbol (str): instrument name
            price_value (str): set price value
            is_override (str, optional): override "true"/"false". Defaults to "true".

        Returns:
            bool: set success or failed
        """
        instrument_id = self.get_instrument_id(instrument_symbol)
        set_response = self.set_valuation_override(
            instrument_id=instrument_id,
            field=ValuationNodeFieldEnum.INDEX_PRICE,
            is_override=is_override,
            value=price_value,
        )
        for each_result in set_response:
            try:
                if not each_result.success:
                    logger.warning(f"set mark price failed, target host ip is {each_result.host}")
                    return False
            except IndexError:
                return False
            except KeyError:
                return False
            except Exception as e:
                logger.error("set index price failed!")
                logger.error(str(e))
                return False
        return True

    def get_detail_valuation_value_by_instrument(self, instrument_symbol: str, field: ValuationNodeFieldEnum):
        """
        get valuation value by instrument symbol
        @param instrument_symbol
        @param field
        """
        instrument_id = self.get_instrument_id(instrument_symbol)
        response = self.get_valuation_result(instrument_id)
        shard_name = SHARD_NAMES.market_data[0]
        index = self._get_result_index_in_admin_help(
            shard_name=shard_name,
            node_name=MarketDataSystemNameEnum.VALUATION_NODE.value,
            method=ValuationNodeMethodEnum.getValuationResult.value,
            index_name="Value",
        )
        return self._get_valuation_value_from_response(response, field, index=index)

    def get_index_price(self, instrument_symbol: str):
        """get instrument index price

        Args:
            instrument_symbol (str): instrument name

        Returns:
            _type_: _description_
        """
        return self.get_detail_valuation_value_by_instrument(instrument_symbol, ValuationNodeFieldEnum.INDEX_PRICE)
