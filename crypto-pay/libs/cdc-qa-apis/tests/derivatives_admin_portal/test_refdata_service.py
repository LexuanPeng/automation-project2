import pytest
from cdc.qa.apis.derivatives_admin_portal import AdminPortalServices
from .mocks import mock_get_config  # noqa


@pytest.mark.parametrize(
    "currency,product",
    [
        ("DAI", "product00a01"),
        ("CRO", "product00a01"),
        ("ETH", "product01a01"),
        ("AVAX", "product01a01"),
    ],
)
def test_global_get_config(mock_get_config, currency, product):
    ser = AdminPortalServices().global_data
    shard_name = ser.refdata_service.get_product_shard_name(currency)
    assert shard_name == product
