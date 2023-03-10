import subprocess
from abc import ABC, abstractmethod
from typing import Union
import logging
import time
import paramiko
import re

logger = logging.getLogger(__name__)


class ConsoleInteractive(ABC):
    """An abstract class for implementing an interactive console with SSH client.

    Attributes:
        before (str): Content before the expected was matched. See `expect`.
    """

    SHELL_PROMPT = re.compile(r"(\[.* ~\]\$ )|(-bash-.*)")

    def __init__(self, ssh_config: dict):
        """Inits ConsoleInteractive.

        Args:
            ssh_config (dict): dict mapping of SSH config used in connection.
        """
        self._ssh_config = ssh_config
        self._client: paramiko.SSHClient = paramiko.SSHClient()
        self._client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self._channel: paramiko.Channel
        self._write_buffer: str = ""
        self._read_buffer: str = ""

        self.before: str = ""

        self.check_gpg_agent()
        self.connect_ssh(self._ssh_config)
        self.access_console()

    def shutdown(self):
        """Shutdown the SSH client connection."""
        self._client.close()
        logger.info("SSH client connection closed.")

    @staticmethod
    def check_gpg_agent():
        """Check if GPG agent is used during SSH connection.

        If GPG agent is used, ensure that GPG agent is responsive and restart GPG agent if not.
        """

        if "gpg-agent" in subprocess.run(["echo $SSH_AUTH_SOCK"], shell=True, capture_output=True, text=True).stdout:
            logger.debug("Using GPG agent for SSH, checking if GPG agent is working properly...")
            try:
                if (
                    "cardno:"
                    not in subprocess.run(["ssh-add -l"], shell=True, capture_output=True, text=True, timeout=10).stdout
                ):
                    raise ValueError("GPG public ssh key not found.")
            except (subprocess.TimeoutExpired, ValueError):
                logger.debug("GPG agent is not working properly, restarting GPG agent...")
                subprocess.run(
                    [
                        "pkill -9 gpg-agent && "
                        "export SSH_AUTH_SOCK=$(gpgconf --list-dirs agent-ssh-socket) && "
                        "gpgconf --launch gpg-agent"
                    ],
                    shell=True,
                )
                logger.debug("GPG agent restarted.")
        else:
            logger.debug("Not using GPG agent...")

    def connect_ssh(self, ssh_config: dict):
        """Connect the SSH client with the given config.

        Args:
            ssh_config (dict): dict mapping of SSH config.
        """

        self._client.connect(**ssh_config, timeout=30, banner_timeout=30)
        logger.info(f"SSH client connected to host '{ssh_config['hostname']}'.")
        self._channel = self._client.invoke_shell()

    def write(self, s: str, timeout: int = 10):
        """Attempt to send to the SSH client.

        Args:
            s (str): Content to be written.
            timeout (int, optional): Time in seconds before aborting the attempt. Defaults to 10.
        """
        self._write_buffer += s

        time_limit = time.time() + timeout
        while time.time() < time_limit:
            if self._channel.send_ready():
                self._channel.send(self._write_buffer.encode("utf-8"))
                self._write_buffer = ""
                break
            time.sleep(0.5)

    def expect(self, *args: Union[str, re.Pattern], timeout: int = 60) -> str:
        """Attempt to wait for the given pattern to be received from the SSH client.

        This will return the string that matched the given patterns, while content before the match will be stored in
        the class attribute `before`. Content after the match will remains in buffer.

        Args:
            *args (Union[str, re.Pattern]): Patterns to be matched.
            timeout (int, optional): Time in seconds before aborting the attempt. Defaults to 60.

        Raises:
            TimeoutError: Timeout while waiting for the expected patterns.

        Returns:
            str: String received from SSH client matching any of the given patterns.
        """
        patterns = [arg.pattern if isinstance(arg, re.Pattern) else re.escape(arg) for arg in args]
        pattern = rf"^(?P<before>[\s\S]*)(?P<expected>{'|'.join(patterns)})(?P<after>[\s\S]*)$"
        matcher = re.compile(pattern)

        time_limit = time.time() + timeout
        while time.time() < time_limit:
            if self._channel.recv_ready():
                self._read_buffer += self._channel.recv(nbytes=1024).decode("utf-8")

                match = matcher.match(self._read_buffer)
                if match:
                    self.before = match.group("before")
                    self._read_buffer = match.group("after")
                    return match.group("expected")
            time.sleep(0.5)
        else:
            logger.warning(
                f"""
                expect() timeout after {timeout}s.
                Matching pattern: {matcher.pattern}
                Current buffer: {self._read_buffer}
                """
            )
            raise TimeoutError

    def shell_prompt(self, *args, **kwargs) -> str:
        """Shorthand for expecting a shell prompt. See `expect`."""
        return self.expect(self.SHELL_PROMPT, *args, **kwargs)

    @abstractmethod
    def console_prompt(self, *args, **kwargs) -> str:
        """Abstract method for expecting the console prompt."""
        pass

    @abstractmethod
    def access_console(self):
        """Abstract method for accessing the console."""
        pass

    @abstractmethod
    def is_alive(self) -> bool:
        """Abstract method for checking if the console is alive."""
        pass
