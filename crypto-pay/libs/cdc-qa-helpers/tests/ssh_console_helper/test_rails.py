import pytest
from cdc.qa.helpers.ssh_console_helper import rails


@pytest.mark.slow
def test_instantiate():
    assert rails.RailsConsoleHelper()
