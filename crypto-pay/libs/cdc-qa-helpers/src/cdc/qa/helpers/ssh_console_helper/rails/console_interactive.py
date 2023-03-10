import os
import re
import logging
import socket

from ..console_interactive import ConsoleInteractive
from ..exceptions import NoSuchContainerException

logger = logging.getLogger(__name__)


class RailsConsoleInteractive(ConsoleInteractive):
    """An encapsulation of interactive rails console with SSH client.

    Attributes:
        before (str): Content before the expected was matched. See `expect`.
    """

    CONSOLE_PROMPT = re.compile(r"irb\(main\):.*:0> ")
    ERROR_NO_SUCH_CONTAINER = "Error: No such container"

    def console_prompt(self, *args, **kwargs) -> str:
        """Shorthand for expecting a rails prompt. See `expect`."""
        return self.expect(self.CONSOLE_PROMPT, *args, **kwargs)

    def access_console(self):
        """Access the rails console over SSH client.

        Raises:
            NoSuchContainerException: Rails console container not found on connected SSH client.
        """
        CONTAINER_NAME = os.environ.get("RAILS_CONSOLE_CONTAINER_NAME", "StagingA-user-batch-job-worker")

        self.shell_prompt(timeout=30)
        self.write(
            f"""
            container=$(docker ps | grep {CONTAINER_NAME} | awk 'NR==1{{print $1}}')
            docker exec -e COLUMNS="`tput cols`" -e LINES="`tput lines`" -ti "${{container}}" bash -c 'env NI2C_LOG=1 /usr/bin/env bash'
            source .aws-env
            bin/rails console -- --nomultiline --nocolorize
            """  # noqa: E501
        )
        if self.console_prompt(self.ERROR_NO_SUCH_CONTAINER, timeout=30) == self.ERROR_NO_SUCH_CONTAINER:
            logger.warning("Failed to access rails console: No such container")
            self.shutdown()
            raise NoSuchContainerException

    def is_alive(self) -> bool:
        """Check if the rails console is alive.

        Returns:
            bool: State of the rails console.
        """
        try:
            self.write("\n")
        except socket.error:
            return False

        try:
            self.console_prompt(timeout=10)
            return True
        except TimeoutError:
            return False
