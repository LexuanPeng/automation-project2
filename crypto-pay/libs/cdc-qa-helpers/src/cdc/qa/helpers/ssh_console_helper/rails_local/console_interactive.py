import os
import re
import logging
from ..rails.console_interactive import RailsConsoleInteractive as BaseRailsConsoleInteractive
from ..exceptions import NoSuchContainerException

logger = logging.getLogger(__name__)


class RailsConsoleInteractive(BaseRailsConsoleInteractive):

    """An encapsulation of interactive rails console with SSH client.
    Attributes:
        before (str): Content before the expected was matched. See `expect`.
    """

    SHELL_PROMPT = re.compile(r"(\[.* ~\]\$ )|(bash-.*)|(.*?:\~\$.*?)")

    def access_console(self):
        """Access the rails console over SSH client.
        Raises:
            NoSuchContainerException: Rails console container not found on connected SSH client.
        """
        CONTAINER_NAME = os.environ.get("RAILS_CONSOLE_CONTAINER_NAME", "app_run")

        self.write(
            """
            bash
            """
        )
        self.shell_prompt(timeout=30)
        self.write(
            f"""
            container=$(docker ps | grep {CONTAINER_NAME} | awk 'NR==1{{print $1}}')
            docker exec -e COLUMNS="`tput cols`" -e LINES="`tput lines`" -ti "${{container}}" bash -c 'env NI2C_LOG=1 /usr/bin/env bash'
            bin/rails console -- --nomultiline --nocolorize
            """  # noqa: E501
        )
        if self.console_prompt(self.ERROR_NO_SUCH_CONTAINER, timeout=45) == self.ERROR_NO_SUCH_CONTAINER:
            logger.warning("Failed to access rails console: No such container")
            self.shutdown()
            raise NoSuchContainerException
