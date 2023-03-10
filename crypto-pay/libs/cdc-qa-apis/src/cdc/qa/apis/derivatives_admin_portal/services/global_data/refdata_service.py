import json
import logging

from ..admin import AdminBaseService, SHARD_NAMES
from ...models.global_model import GlobalSystemNameEnum, RefDataServiceMethodEnum
from ...models.exceptions import GetProductConfigException, GetConfigException

logger = logging.getLogger(__name__)


class RefDataService(AdminBaseService):
    def get_config(self, name: str = "SEQ2_NETWORK", target_host_ip: str = GlobalSystemNameEnum.REFDATA_SERVICE.value):
        arguments = {"name": name}
        try:
            get_config = self._admin(
                shard_name=SHARD_NAMES.global_shard,
                command=RefDataServiceMethodEnum.getConfig,
                target=target_host_ip,
                arguments=arguments,
            )
            return get_config[0]
        except Exception as e:
            logger.error("get config failed!")
            logger.error(str(e))
            raise GetConfigException("Get Config failed!")

    def get_product_shard_name(self, currency: str):
        try:
            config_result = self.get_config().result
            config_json_result = json.loads(config_result)[0]
            config_info = json.loads(config_json_result[1])
            cluster_shard_info_list = config_info["clusterShardInfoList"]
            hosts = []
            for each_shard_info in cluster_shard_info_list:
                if each_shard_info["clusterType"] == "PRODUCT":
                    product_shard_details = each_shard_info["shardDetails"]
                    for shard_detail in product_shard_details:
                        filter_data_details = shard_detail["filterDataDetails"]
                        for each_data in filter_data_details:
                            currencies = each_data.split(",")
                            for each_currency in currencies:
                                current_currency = each_currency.split("|")[0]
                                if currency.upper() == current_currency.upper():
                                    hosts = shard_detail["hosts"]
                                    break
                        if hosts:
                            break
                    if hosts:
                        break
            if not hosts:
                logger.error(
                    f"Failed to find currency {currency} in get config response, "
                    f"getConfig result is {config_result}"
                )
                raise GetProductConfigException(
                    f"Failed to find currency {currency} in get config response, "
                    f"getConfig result is {config_result}"
                )
            else:
                product_host = hosts[0]
                return product_host

        except Exception as e:
            logger.info("get product by instrument name failed!")
            logger.error(str(e))
            raise GetProductConfigException("get product by currency failed!")
