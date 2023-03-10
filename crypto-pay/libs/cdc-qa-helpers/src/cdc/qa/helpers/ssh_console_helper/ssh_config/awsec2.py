from __future__ import annotations

from .base import SSHConfig

from collections import namedtuple
import boto3
import paramiko

import logging

logger = logging.getLogger(__name__)
ec2 = boto3.client("ec2")


NodeDef = namedtuple("node_def", ["host_prefix", "node_name", "bastion_name"])


class AWSEC2SSHConfig(SSHConfig):
    """Class for storing and resolving SSH configs by getting instances info from AWS EC2."""

    def __init__(self, node_defs: list[dict]):
        """Inits AWSEC2SSHConfig.

        Args:
            nodes_def (list[dict]): A list of node definitions to get SSH configs from.
        """
        self._config: dict[str, dict] = self._get_config([NodeDef(**node_def) for node_def in node_defs])

    @staticmethod
    def _get_config(node_defs: list[NodeDef]) -> dict[str, dict]:
        config = {}

        for node_def in node_defs:
            host_prefix = node_def.host_prefix
            node_name = node_def.node_name
            bastion_name = node_def.bastion_name

            # get bastion instances info
            bastion_instances_info = ec2.describe_instances(Filters=[{"Name": "tag:Name", "Values": [bastion_name]}])
            bastion_instances = bastion_instances_info["Reservations"][0]["Instances"]
            bastion_ip = bastion_instances[0]["PrivateIpAddress"]
            config[f"{host_prefix}-bastion"] = {"hostname": bastion_ip, "username": "ec2-user"}

            # get node instances info
            node_instances_info = ec2.describe_instances(Filters=[{"Name": "tag:Name", "Values": [node_name]}])
            node_instances = (instance for res in node_instances_info["Reservations"] for instance in res["Instances"])
            for count, node_instance in enumerate(node_instances, start=1):
                node_config = {}
                node_config["hostname"] = node_instance["PrivateIpAddress"]
                node_config["username"] = "ec2-user"
                node_config["proxyjump"] = f"{host_prefix}-bastion"
                config[f"{host_prefix}{count}"] = node_config

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

        if "proxyjump" in host_config:
            proxy_client = paramiko.SSHClient()
            proxy_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            proxy_client.connect(**self.resolve_ssh_config(host_config["proxyjump"]), timeout=10)
            proxy_transport = proxy_client.get_transport()
            if proxy_transport:
                config["sock"] = proxy_transport.open_channel("direct-tcpip", (config["hostname"], 22), ("", 0))

        config = {**config, **kwargs}

        return config
