from __future__ import annotations

import os
import logging

from ..constants import SSH_CONFIG_PATH
from ..rails.console_helper import RailsConsoleHelper as BaseRailsConsoleHelper
from ..ssh_config import FileSSHConfig
from .console_interactive import RailsConsoleInteractive
from ..exceptions import FailedToStartConsoleException
from retry import retry


logger = logging.getLogger(__name__)


class RailsConsoleHelper(BaseRailsConsoleHelper):
    """A helper class that handles actions through executing commands on rails console."""

    def shutdown(self):
        self.stop_console()

    def start_console(self, tries: int = 5):
        """Attempt to start a `RailsConsoleInteractive` instance.
        Args:
            tries (int): Number of retry for each start method upon failing to start the console on all hosts.
        Raises:
            FailedToStartConsoleException: Cannot start a rails console on any of the defined hosts.
        """

        @retry(FailedToStartConsoleException, tries=tries)
        def start_from_local():
            hostname = os.environ.get("LOCAL_RAILS_HOST_NAME", "localhost")
            try:
                logger.info(f"Starting rails console on '{hostname}'...")
                config = FileSSHConfig(SSH_CONFIG_PATH)
                host = config.resolve_ssh_config(hostname=hostname)
                self.console = RailsConsoleInteractive(host)
                logger.info(f"Rails console started on '{hostname}'.")
            except Exception as e_:
                logger.warning(f"Failed to start rails console on 'localhost': {e_}")
                try:
                    self.console.shutdown()
                except Exception:
                    pass

        start_methods = list()
        start_methods.append(start_from_local)

        for method in start_methods:
            try:
                method()
                break
            except Exception as e:
                logger.error(f"{method=} encountered exception: {e}")
        else:
            raise FailedToStartConsoleException
