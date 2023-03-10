import os

import urllib3
from pydantic import BaseModel, Field
from dataclasses import dataclass, field
from typing import Optional, Any
import logging

from requests.auth import AuthBase

from cdc.qa.apis.common.models.rest_api import RestApi
from cdc.qa.apis.common.services.rest_service import RestService


logger = logging.getLogger(__name__)


class FrozenBaseModel(BaseModel):
    class Config:
        frozen = True


def encrypt_passcode(passcode) -> str:
    from cdc.qa.core import secretsmanager as sm
    import base64
    import binascii
    import hashlib
    import hmac
    import random
    import time
    import string
    from Crypto.Cipher import AES
    from Crypto.Random import get_random_bytes
    from Crypto.Util import Padding

    secret_key = os.environ.get("PASSCODE_ENCRYPTION_KEY", None)
    secret_key = secret_key or sm.get_secret_json("railsapi")["PASSCODE_ENCRYPTION_KEY"]
    secret_key = binascii.unhexlify(secret_key)
    _IV = get_random_bytes(16)
    cipher_aes = AES.new(secret_key, AES.MODE_CBC, _IV)

    random_string = "".join(random.choices(string.ascii_lowercase + string.digits, k=20))
    timestamp = int(time.time())
    text_to_be_encrypted = f"{passcode}-{timestamp}-{random_string}"

    encrypted_data = cipher_aes.encrypt(Padding.pad(text_to_be_encrypted.encode("utf-8"), 16))
    base64_encrypted_text = base64.b64encode(encrypted_data)
    base64_encrypted_iv = base64.b64encode(_IV)
    blob = base64_encrypted_text + b"--" + base64_encrypted_iv
    data = base64.b64encode(blob)
    hashed = hmac.new(secret_key, data, hashlib.sha1)
    encrypted_passcode = data + b"--" + str.encode(hashed.hexdigest())
    encrypted_passcode = encrypted_passcode.decode("utf-8")

    logger.debug(f"Encrypted: '{text_to_be_encrypted}' -> '{encrypted_passcode}")
    return encrypted_passcode


class RailsEncryptedPasscodeRequest(FrozenBaseModel):
    passcode: str = Field()

    def __init__(self, **data: Any):
        super().__init__(**data)
        object.__setattr__(self, "passcode", encrypt_passcode(self.passcode))


class RailsResponse(FrozenBaseModel):
    ok: bool = Field()
    error: Optional[str] = Field()


class RailsResponseError(Exception):
    pass


@dataclass(frozen=True)
class RailsRestApi(RestApi):
    log_filters = ["x_csrf_token", "token", "secret_key", "password", "2fa", "2fa_code", "otp_secret"]

    def __post_init__(self):
        urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@dataclass(frozen=True)
class RailsRestService(RestService):
    env: str = field(default="stg")
    secret_id: str = field(default="railsapi")


class BearerAuth(AuthBase):
    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r
