import re
import logging
import socket

from ..console_interactive import ConsoleInteractive
from ..exceptions import NoSuchContainerException

logger = logging.getLogger(__name__)


class FiatConsoleInteractive(ConsoleInteractive):
    """An encapsulation of interactive fiat console with SSH client.

    Attributes:
        before (str): Content before the expected was matched. See `expect`.
    """

    CONSOLE_PROMPT = re.compile(r"irb\(main\):.*:0> ")
    ERROR_NO_SUCH_CONTAINER = "Error: No such container"

    def console_prompt(self, *args, **kwargs) -> str:
        """Shorthand for expecting a fiat prompt. See `expect`."""
        return self.expect(self.CONSOLE_PROMPT, *args, **kwargs)

    def access_console(self):
        """Access the fiat console over SSH client.

        Raises:
            NoSuchContainerException: Rails console container not found on connected SSH client.
        """
        self.shell_prompt(timeout=30)
        self.write(
            """
            container=$(docker ps | grep crypto-fiat | awk 'NR==1{print $1}')
            docker exec -e COLUMNS="`tput cols`" -e LINES="`tput lines`" -ti "${container}" bash -c 'env NI2C_LOG=1 /usr/bin/env bash'
            source .aws-env
            bin/spring stop
            bin/rails console -- --nomultiline --nocolorize
            """  # noqa: E501
        )
        if self.console_prompt(self.ERROR_NO_SUCH_CONTAINER, timeout=30) == self.ERROR_NO_SUCH_CONTAINER:
            logger.warning("Failed to access fiat console: No such container")
            self.shutdown()
            raise NoSuchContainerException

    def is_alive(self) -> bool:
        """Check if the fiat console is alive.

        Returns:
            bool: State of the fiat console.
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
