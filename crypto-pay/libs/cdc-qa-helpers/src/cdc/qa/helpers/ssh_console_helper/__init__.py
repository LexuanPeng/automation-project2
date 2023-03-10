"""Helpers for SSH Console related operations.

This module includes 2 major types of classes: `ConsoleInteractive` as an encapsulation for handling SSH client related
operations, `ConsoleHelper` for handling usage commands using the aforementioned `ConsoleInteractive` class.

Available `ConsoleInteractive`:
    RailsConsoleInteractive
    FiatConsoleInteractive

Available `ConsoleHelper`:
    RailsConsoleHelper
    FiatConsoleHelper


Usage example:

    rails_console_helper = RailsConsoleHelper()
    result = rails_console_helper.exec_command("command.to.be.executed")
"""

from .rails import RailsConsoleInteractive, RailsConsoleHelper
from .rails_local import (
    RailsConsoleInteractive as LocalRailsConsoleInteractive,
    RailsConsoleHelper as LocalRailsConsoleHelper,
)
from .fiat import FiatConsoleInteractive, FiatConsoleHelper
from .exchange_rails import ExchangeRailsConsoleHelper

__all__ = [
    "RailsConsoleInteractive",
    "RailsConsoleHelper",
    "FiatConsoleInteractive",
    "FiatConsoleHelper",
    "ExchangeRailsConsoleHelper",
    "LocalRailsConsoleInteractive",
    "LocalRailsConsoleHelper",
]
