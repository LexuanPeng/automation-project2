from __future__ import annotations

from .base import SSHConfig

from collections import namedtuple
import paramiko
import io
import os
import tempfile
import time

from cdc.qa.core import secretsmanager as sm

import logging

logger = logging.getLogger(__name__)

NodeDef = namedtuple("node_def", ["hostname", "user", "tsh_proxy", "tsh_cluster", "tsh_port"])


class TSHUserNotFoundException(Exception):
    pass


class TSHSSHConfig(SSHConfig):
    """Class for storing and resolving SSH configs for Teleport(TSH)."""

    def __init__(self, node_defs: list[dict]):
        """Inits TSHSSHConfig.

        Args:
            node_defs (list[dict]): A list of node definitions to get SSH configs from.
        """
        self._config: dict[str, dict] = self._get_config([NodeDef(**node_def) for node_def in node_defs])

    @staticmethod
    def _get_config(node_defs: list[NodeDef]) -> dict[str, dict]:
        config = {}

        for node_def in node_defs:
            hostname = node_def.hostname
            user = node_def.user
            tsh_proxy = node_def.tsh_proxy
            tsh_cluster = node_def.tsh_cluster
            tsh_port = node_def.tsh_port

            config[hostname] = {
                "hostname": hostname,
                "username": user,
                "tsh_proxy": tsh_proxy,
                "tsh_cluster": tsh_cluster,
                "tsh_port": tsh_port,
            }

        return config

    @property
    def hostnames(self) -> set[str]:
        return set(self._config.keys())

    def resolve_ssh_config(self, hostname: str, **kwargs) -> dict:
        host_config = self._config[hostname]

        config = {}

        if "hostname" in host_config:
            config["hostname"] = host_config.get("hostname")
        if "username" in host_config:
            config["username"] = host_config.get("username")

        pkey = paramiko.RSAKey.from_private_key(
            io.StringIO(sm.get_secret_binary(f"teleport/{host_config['tsh_proxy']}/pkey").decode())
        )
        pkey.load_certificate(
            sm.get_secret_binary(f"teleport/{host_config['tsh_proxy']}/{host_config['tsh_cluster']}/ssh-cert").decode()
        )

        config["pkey"] = pkey
        config["look_for_keys"] = False
        config["disabled_algorithms"] = {"pubkeys": ["rsa-sha2-512", "rsa-sha2-256"]}

        tmp_pem = tempfile.NamedTemporaryFile(mode="w+b", delete=False)
        try:
            tmp_pem.write(sm.get_secret_binary(f"teleport/{host_config['tsh_proxy']}/identity"))
            tmp_pem.close()
            config["sock"] = paramiko.ProxyCommand(
                f"tsh -i {tmp_pem.name} proxy ssh --proxy={host_config['tsh_proxy']} --cluster={host_config['tsh_cluster']} {host_config['username']}@{hostname}:{host_config['tsh_port']}"  # noqa:E501
            )
            time.sleep(1)  # wait identity file to load into memory of proxycommand
        finally:
            os.unlink(tmp_pem.name)

        config = {**config, **kwargs}

        return config
