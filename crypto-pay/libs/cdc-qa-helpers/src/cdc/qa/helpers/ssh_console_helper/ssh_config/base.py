from __future__ import annotations

from abc import ABC, abstractmethod


class SSHConfig(ABC):
    @property
    @abstractmethod
    def hostnames(self) -> set[str]:
        """A set of hostnames defined in this `SSHConfig`."""
        pass

    @abstractmethod
    def resolve_ssh_config(self, hostname: str, **kwargs) -> dict:
        """Resolve the required config used in connecting SSH client.

        Args:
            hostname (str): Hostname of the server used in resolving config.
            **kwargs: Other arguments to be merged with the resolved config.

        Returns:
            dict: The resolved config mapped in dict.
        """
        pass
