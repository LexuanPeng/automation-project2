from __future__ import annotations
from typing import Callable, TYPE_CHECKING

from abc import ABC, abstractmethod
import logging
import functools

if TYPE_CHECKING:
    from .console_interactive import ConsoleInteractive

logger = logging.getLogger(__name__)


def auto_reconnect(method: Callable) -> Callable:
    """Decorator for auto reconnecting rails console if it is not alive."""

    @functools.wraps(method)
    def wrapper(self: ConsoleHelper, *args, **kwargs):
        if not self.console.is_alive():
            logging.info("Console is not alive, reconnecting...")
            self.console.shutdown()
            self.start_console()
        return method(self, *args, **kwargs)

    return wrapper


class ConsoleHelper(ABC):
    """An abstract class for implementing console helper."""

    def __init__(self):
        """Init ConsoleHelper.

        Attributes:
            console (ConsoleInteractive): Connected `ConsoleInteractive` for executing commands.
        """
        self.console: ConsoleInteractive
        self.start_console()

    @abstractmethod
    def start_console(self):
        """An abstract method for starting the console."""
        pass

    def stop_console(self):
        """Stop the console."""
        self.console.shutdown()

    @auto_reconnect
    def exec_command(self, command: str, hide_command: bool = True, wrap_with_begin: bool = False) -> str:
        """Execute command on console.
        Remarks:
            'wrap_with_begin' option is only applicable in rails application console
            if add any ssh console for other programming language, should rewrite this function and extract 'wrap_with_begin' option

        Args:
            command (str): Command to be executed.
            hide_command (bool, optional): Hide the executed command from the received content. Defaults to True.
            wrap_with_begin (bool, optional): Wrap the execute command with 'begin' block. Only used in rails application console. Defaults to False

        Returns:
            str: Content received from executing the command.
        """  # noqa: E501
        command = command.strip()
        if wrap_with_begin:
            command = f"""
            begin
                {command}
            end
            """.strip()
        self.console.write(f"{command}\n")
        self.console.console_prompt()
        result = self.console.before
        if hide_command:
            result = result.replace(command, "").lstrip()
        return result
