from __future__ import annotations

from .base import SSHConfig

from collections import namedtuple
import boto3
import paramiko

import logging

logger = logging.getLogger(__name__)
ec2 = boto3.client("ec2")
ecs = boto3.client("ecs")


ServiceDef = namedtuple("service_def", ["host_prefix", "cluster_name", "service_name", "bastion_name"])


class AWSECSSSHConfig(SSHConfig):
    """Class for storing and resolving SSH configs by getting instances info from AWS ECS."""

    def __init__(self, service_defs: list[dict]):
        """Inits AWSECSSSHConfig.

        Args:
            service_defs (list[dict]): A list of service definitions to get SSH configs from.
        """
        self._config: dict[str, dict] = self._get_config([ServiceDef(**service_def) for service_def in service_defs])

    @staticmethod
    def _get_config(service_defs: list[ServiceDef]) -> dict[str, dict]:
        config = {}

        for service_def in service_defs:
            host_prefix = service_def.host_prefix
            cluster_name = service_def.cluster_name
            service_name = service_def.service_name
            bastion_name = service_def.bastion_name

            # get bastion instances info
            bastion_instances_info = ec2.describe_instances(Filters=[{"Name": "tag:Name", "Values": [bastion_name]}])
            bastion_instances = bastion_instances_info["Reservations"][0]["Instances"]
            bastion_ip = bastion_instances[0]["PrivateIpAddress"]
            config[f"{host_prefix}-bastion"] = {"hostname": bastion_ip, "username": "ec2-user"}

            # get service instances info
            service_task_arns = ecs.list_tasks(
                cluster=cluster_name,
                serviceName=service_name,
                desiredStatus="RUNNING",
                launchType="EC2",
            )["taskArns"]
            service_tasks = ecs.describe_tasks(cluster=cluster_name, tasks=service_task_arns)["tasks"]
            service_container_instance_arns = [task["containerInstanceArn"] for task in service_tasks]
            service_container_instances = ecs.describe_container_instances(
                cluster=cluster_name,
                containerInstances=service_container_instance_arns,
            )["containerInstances"]
            ec2_instance_ids = [instance["ec2InstanceId"] for instance in service_container_instances]

            ec2_instance_info = ec2.describe_instances(Filters=[{"Name": "instance-id", "Values": ec2_instance_ids}])
            ec2_instances = (instance for res in ec2_instance_info["Reservations"] for instance in res["Instances"])
            for count, node_instance in enumerate(ec2_instances, start=1):
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
