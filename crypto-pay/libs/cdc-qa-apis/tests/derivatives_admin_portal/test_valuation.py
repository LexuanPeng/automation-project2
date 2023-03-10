import json
import logging

import pytest
from cdc.qa.apis.derivatives_admin_portal import AdminPortalServices
from pydantic.error_wrappers import ValidationError

from .mocks import mock_admin_get_account_id, mock_admin_help_placeholder, mock_all_ps_admin_instrument_id  # noqa
from .mocks import mock_admin_transfer_to_deriv, mock_incorrect_admin_help_placeholder  # noqa
from .mocks import mock_admin_global_get_account_shard_name  # noqa

logging.basicConfig(level=logging.DEBUG)


def test_get_instrument_id(mock_admin_help_placeholder):
    ser = AdminPortalServices().product
    instr_id = ser.valuation_node.get_instrument_id("BTCUSD-PERP")

    assert instr_id == 303


def test_invalid_admin_placeholder_response(mock_incorrect_admin_help_placeholder):
    ser = AdminPortalServices().product
    with pytest.raises(ValidationError) as execinfo:
        ser.valuation_node.get_instrument_id("BTCUSD-PERP")
    raw_errors = execinfo.value.raw_errors
    value_error = [
        error
        for error in raw_errors
        if (not isinstance(error, list))
        and isinstance(error.exc, ValueError)
        and "original content:" in error.loc_tuple()
    ][0]
    error_info = json.loads(value_error.exc.args[0])
    assert error_info[0].get("instId2") == 306


def test_get_account_id(mock_admin_get_account_id):
    ser = AdminPortalServices().account
    user_account_details = ser.account_service.get_user_account_details(email="leen.li+sz01@crypto.com")[0].result
    details_list = json.loads(user_account_details)
    user_account_id = details_list[0][0]
    assert user_account_id == "96a0d316-3e6c-402b-8a9a-57c543d11861"


def test_transfer_to_deriv(
    mock_admin_transfer_to_deriv,
    mock_admin_get_account_id,
    mock_all_ps_admin_instrument_id,
):
    ser = AdminPortalServices().account
    account_id = ser.account_service.get_user_account_id_by_email("leen.li+sz01@crypto.com")
    transfer_results = ser.position_service.user_transfer_to_wallet(
        account_id=account_id,
        instrument_name="USD_Stable_Coin",
        qty_delta="100",
        cost_delta="100",
    )
    assert transfer_results
