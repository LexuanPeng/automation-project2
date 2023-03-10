import json
import logging

import urllib3

from ...models.admin import AdminResponse
from ...models.exceptions import NotFoundException
from ...models.product import (
    ProductSystemNameEnum,
    ValuationNodeFieldEnum,
    ValuationNodeMethodEnum,
    ValuationNodeProfileEnum,
)
from ..admin import AdminBaseService
from ..global_data import GlobalServices

urllib3.disable_warnings()
logger = logging.getLogger(__name__)


class ValuationNodeService(AdminBaseService):
    def _get_valuation_value_from_response(
        self, valuation_resp: AdminResponse, field: ValuationNodeFieldEnum, index: int
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
        target_host_ip: str = ProductSystemNameEnum.VALUATION_NODE.value,
        shard_names: list = ["product00a01"],
    ) -> AdminResponse:
        """
        Set Valuation Override
        @param instrument_id: instrument id
        @param field: MARK_PRICE, INDEX_PRICE, FAIR_PRICE, FUNDING_RATE
        @param is_override: true/false
        @param value: string, the value for field
        @param target_host_ip: you can get the target_host_ip by get_target_host_ip(system_name)
        @param shard_names: shard names can be ["product00a01", "product01a01"]
        @param profile: LIVE_EXCHANGE_OFFICIAL, LIVE_RISK_OFFICIAL, LIVE_TRADING_OFFICIAL, HOURLY_RISK_SMART_MARGIN,
        RESERVED_FOR_RISK_PORTFOLIO_MARGIN, RESERVED_FOR_RISK_PORTFOLIO_MARGIN_2
        """
        if not target_host_ip:
            target_host_ip = ProductSystemNameEnum.VALUATION_NODE.value
        arguments = {
            "instrument": instrument_id,
            "profile": profile.value,
            "field": field.value,
            "override": is_override,
            "value": value,
        }

        set_valuation_result = None
        res_list = []
        # set valuation on each shard
        for shard_name in shard_names:
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

    def get_valuation_result(
        self,
        instrument_id,
        target_host_ip: str = ProductSystemNameEnum.VALUATION_NODE.value,
        shard_names: list = ["product00a01"],
    ):
        """
        Get valuation result by instrument id and target host ip
        """
        if not target_host_ip:
            target_host_ip = ProductSystemNameEnum.VALUATION_NODE.value
        arguments = {"instrument": instrument_id}
        for shard_name in shard_names:
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

    def get_product_shard_name_by_instrument_name(self, instrument_name: str):
        if "_" in instrument_name:
            currency = instrument_name.split("_")[0]
        else:
            instrument_prefix = instrument_name.split("-")[0]
            currency = instrument_prefix[: instrument_prefix.index("USD")]
        shard_name = GlobalServices(self.host).refdata_service.get_product_shard_name(currency=currency)
        return shard_name

    def set_mark_price(self, instrument_symbol: str, price_value: str = None, is_override: str = "true"):
        instrument_id = self.get_instrument_id(instrument_symbol)
        shard_name = self.get_product_shard_name_by_instrument_name(instrument_name=instrument_symbol)
        set_response = self.set_valuation_override(
            instrument_id=instrument_id,
            field=ValuationNodeFieldEnum.MARK_PRICE,
            is_override=is_override,
            value=price_value,
            shard_names=[shard_name],
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
                logger.error("set mark price failed!")
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
        shard_name = self.get_product_shard_name_by_instrument_name(instrument_name=instrument_symbol)
        response = self.get_valuation_result(instrument_id=instrument_id, shard_names=[shard_name])
        index = self._get_result_index_in_admin_help(
            shard_name=shard_name,
            node_name=ProductSystemNameEnum.VALUATION_NODE.value,
            method=ValuationNodeMethodEnum.getValuationResult.value,
            index_name="Value",
        )
        return self._get_valuation_value_from_response(response, field, index=index)

    def get_mark_price(self, instrument_symbol: str):
        """get MARK PRICE by instrument name

        Args:
            instrument_symbol (str): instrument name

        Returns:
            float: mark price value
        """
        return self.get_detail_valuation_value_by_instrument(instrument_symbol, ValuationNodeFieldEnum.MARK_PRICE)

    def get_fair_price(self, instrument_symbol: str):
        """get FAIR PRICE by instrument name

        Args:
            instrument_symbol (str): instrument name

        Returns:
            float: fair price value
        """
        return self.get_detail_valuation_value_by_instrument(instrument_symbol, ValuationNodeFieldEnum.FAIR_PRICE)
