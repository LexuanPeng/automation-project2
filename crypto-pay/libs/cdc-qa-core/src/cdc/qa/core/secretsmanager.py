import boto3
from botocore.config import Config
from aws_secretsmanager_caching import SecretCache, SecretCacheConfig
import json
from typing import Optional

DEFAULT_PREFIX = "qa-automation/"


config = Config(
    region_name="ap-southeast-1",
)
client = boto3.client("secretsmanager", config=config)
cache = SecretCache(config=SecretCacheConfig(), client=client)


def get_secret(partial_secret_id: str, prefix: Optional[str] = None) -> str:
    """Retrieve a secret as raw string.

    Args:
        partial_secret_id (str): Partial secret id without the prefix.
        prefix (Optional[str], optional): Prefix of the secret id. Defaults to None.

    Returns:
        str: Secret as raw string
    """
    prefix = prefix or DEFAULT_PREFIX
    return cache.get_secret_string(f"{prefix}{partial_secret_id}")


def get_secret_json(partial_secret_id: str, prefix: Optional[str] = None) -> dict:
    """Retrieve a json secret as `dict`, if possible.

    Args:
        partial_secret_id (str): Partial secret id without the prefix.
        prefix (Optional[str], optional): Prefix of the secret id. Defaults to None.

    Raises:
        json.JSONDecodeError: Raised when fails to decode the secret in json.

    Returns:
        dict: Secret as `dict`
    """
    secret_string = get_secret(partial_secret_id, prefix)
    try:
        secret_json = json.loads(secret_string)
        return secret_json
    except json.JSONDecodeError as e:
        raise json.JSONDecodeError(f"{secret_string=}", e.doc, e.pos) from None


def get_secret_binary(partial_secret_id: str, prefix: Optional[str] = None) -> bytes:
    """Retrieve a secret as binary.

    Args:
        partial_secret_id (str): Partial secret id without the prefix.
        prefix (Optional[str], optional): Prefix of the secret id. Defaults to None.

    Returns:
        str: Secret as raw string
    """
    prefix = prefix or DEFAULT_PREFIX
    return cache.get_secret_binary(f"{prefix}{partial_secret_id}")
