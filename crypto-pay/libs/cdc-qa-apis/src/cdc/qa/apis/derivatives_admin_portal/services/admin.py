import json
import logging
from enum import Enum

import urllib3
from cdc.qa.apis.common.models.rest_api import HttpMethods

from ..models.admin import (
    SHARD_NAMES,
    AdminHelpPlaceholderRequestParams,
    AdminHelpPlaceholderResponse,
    AdminHelpResponse,
    AdminRequestBody,
    AdminResponse,
)
from ..models.exceptions import NotFoundException
from ..rest_base import AdminPortalRestApi, AdminPortalRestService

urllib3.disable_warnings()
logger = logging.getLogger(__name__)


class AdminApi(AdminPortalRestApi):
    """admin portal admin/ api"""

    path = "admin/"
    method = HttpMethods.POST
    request_data_type = AdminRequestBody
    response_type = AdminResponse


class AdminHelpAPI(AdminPortalRestApi):
    """admin portal admin/help api"""

    path = "admin/help"
    method = HttpMethods.GET
    response_type = AdminHelpResponse


class AdminHelpPlaceholderAPI(AdminPortalRestApi):
    """admin portal admin/help/placeholder api"""

    path = "admin/help/placeholder"
    method = HttpMethods.GET
    request_params_type = AdminHelpPlaceholderRequestParams
    response_type = AdminHelpPlaceholderResponse


class AdminBaseService(AdminPortalRestService):
    def _admin(
        self,
        shard_name: str,
        command: Enum,
        target: str,
        arguments: dict,
    ) -> AdminResponse:
        host = self._parse_host(shard_name)
        api = AdminApi(host=host, _session=self.session)
        payload = AdminRequestBody(command=command, target=target, arguments=json.dumps(arguments)).json(
            exclude_none=True
        )
        return AdminResponse.parse_raw(b=api.call(data=payload, verify=False).content)

    def _admin_help(self, shard_name: str):
        host = self._parse_host(shard_name=shard_name)
        api = AdminHelpAPI(host=host, _session=self.session)
        return AdminHelpResponse.parse_raw(b=api.call(verify=False).content)

    def _admin_help_placeholder(self, key="ALL_INSTRUMENTS", shard_name: str = SHARD_NAMES.global_shard):
        host = self._parse_host(shard_name=shard_name)
        api = AdminHelpPlaceholderAPI(host=host, _session=self.session)
        params = AdminHelpPlaceholderRequestParams(key=key).dict(exclude_none=True)
        return AdminHelpPlaceholderResponse.parse_raw(b=api.call(params=params, verify=False).content)

    def get_instrument_id(self, instrument_symbol, key="ALL_INSTRUMENTS"):
        """
        Get instrument id by instrument_symbol and key
        @param instrument_symbol: it is the instrument name, such as "ADAUSD-PERP"
        @param key: ALL_TRADABLE_INSTRUMENTS/ALL_PS_INSTRUMENTS
        """
        response_list = self._admin_help_placeholder(key)
        for each_item in response_list:
            if each_item.symbol.lower() == instrument_symbol.lower():
                return each_item.instId
        else:
            raise NotFoundException(f"Failed to find the instrument {instrument_symbol}, key is {key}")

    def _get_result_index_in_admin_help(self, shard_name: str, node_name: str, method: str, index_name: str) -> int:
        try:
            admin_helper_response = self._admin_help(shard_name=shard_name)
            node_response = admin_helper_response.get(node_name)
            method_response = node_response.get(method)
            results = method_response.results
            for index in range(len(results)):
                if results[index].name.upper() == index_name.upper():
                    return index
            else:
                raise NotFoundException(f"Failed to find the name {index_name} in results, results is {results}")
        except Exception as e:
            raise Exception(f"Failed to get {index_name} in results, exception: {e}")
