from __future__ import annotations

from .base import SSHConfig

import paramiko
import io
from pathlib import Path

import logging

logger = logging.getLogger(__name__)


class FileSSHConfig(SSHConfig):
    """Class for storing and resolving SSH configs from a file."""

    def __init__(self, config_path: str):
        """Inits FileSSHConfig.

        Args:
            config_path (str): Path to SSH config file.
        """
        self._config = paramiko.SSHConfig.from_text(self._resolve_include(config_path))

    def _resolve_include(self, config_path: str) -> str:
        """Resolve `Include` statements in config, concatenating the files.

        Args:
            config_path (str): Path to SSH config file.

        Returns:
            str: The resolved config file in string.
        """
        with io.StringIO() as outfile:
            try:
                with open(Path(config_path).expanduser()) as f:
                    for line in f.readlines():
                        if line.startswith("Include "):
                            include_path = line.split()[1]
                            if "*" in include_path:
                                include_glob_paths = Path(config_path).expanduser().parent.glob(include_path)
                                for path in include_glob_paths:
                                    outfile.write(self._resolve_include(str(path)))
                            else:
                                path = Path(config_path).expanduser().parent / include_path
                                outfile.write(self._resolve_include(str(path)))
                        else:
                            outfile.write(line)
            except FileNotFoundError:
                logger.warning(f"File not found in included config path: '{config_path}'")

            return outfile.getvalue()

    @property
    def hostnames(self) -> set[str]:
        return self._config.get_hostnames()

    def resolve_ssh_config(self, hostname: str, **kwargs) -> dict:
        host_config = self._config.lookup(hostname)

        config = {}

        if "hostname" in host_config:
            config["hostname"] = host_config.get("hostname")
        if ("username" in host_config) or ("user" in host_config):
            config["username"] = host_config.get("username") or host_config.get("user")
        if "port" in host_config:
            config["port"] = host_config.get("port")

        if "proxycommand" in host_config:
            config["sock"] = paramiko.ProxyCommand(host_config["proxycommand"])
        elif "proxyjump" in host_config:
            proxy_client = paramiko.SSHClient()
            proxy_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            proxy_client.connect(**self.resolve_ssh_config(host_config["proxyjump"]), timeout=10)
            proxy_transport = proxy_client.get_transport()
            if proxy_transport:
                config["sock"] = proxy_transport.open_channel("direct-tcpip", (config["hostname"], 22), ("", 0))

        config = {**config, **kwargs}

        return config
