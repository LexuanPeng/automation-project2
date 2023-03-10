import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Type, Union, Optional
from urllib.parse import urljoin
import re

import requests
from requests.auth import AuthBase
from pydantic import BaseModel

logger = logging.getLogger(__name__)


class HttpMethods(Enum):
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"


@dataclass(frozen=True)
class RestApi:
    _session: requests.Session = field(default_factory=requests.Session)
    host: str = field(default="")

    path: Union[str, Callable[[BaseModel], str]] = field(init=False, default="")
    method: HttpMethods = field(init=False, default=HttpMethods.GET)
    headers: Optional[dict] = field(init=False, default=None)
    auth: Optional[AuthBase] = field(init=False, default=None)

    path_params_type: Type[BaseModel] = field(init=False, default=BaseModel)
    request_params_type: Type[BaseModel] = field(init=False, default=BaseModel)
    request_data_type: Type[BaseModel] = field(init=False, default=BaseModel)
    response_type: Type[BaseModel] = field(init=False, default=BaseModel)

    log_filters: Optional[list] = field(init=False, default=None)

    def call(
        self,
        *,
        method=None,
        path_params=None,
        params=None,
        data=None,
        headers=None,
        auth=None,
        verify=False,
        timeout=60,
        **kwargs,
    ) -> requests.Response:
        if isinstance(self.path, str):
            path = self.path
        else:
            path = self.path(path_params)
        url = urljoin(self.host, path)
        method = method or self.method.value
        headers = headers or self.headers
        auth = auth or self.auth

        request_info = f"{params=} {data=} {headers=} "
        if self.log_filters:
            request_info = (
                f"params={self.redact(self.log_filters, str(params))} "
                f"data={self.redact(self.log_filters, str(data))} "
                f"headers={self. redact(self.log_filters, str(headers))}"
            )

        logger.debug(f"REST api request: {self.method} {url}")
        logger.debug(f"{request_info} {kwargs=}")
        resp = self._session.request(
            method=method,
            url=url,
            params=params,
            data=data,
            headers=headers,
            auth=auth,
            verify=verify,
            timeout=timeout,
            **kwargs,
        )

        temp_content = resp.content.decode("utf-8")
        if self.log_filters:
            temp_content = self.redact(self.log_filters, temp_content)
        logger.debug(f"REST api response: {resp.status_code} {temp_content}")
        return resp

    @staticmethod
    def redact(patterns, msg):
        if isinstance(msg, str):
            msg = isinstance(msg, str) and msg or str(msg)
            rep_re = r"\g<key_name>\g<mark>\g<link>\g<vmark>******\g<vmark>\g<end>"
            for pattern in patterns:
                match_re = (
                    r"(?P<mark>['\"\\]{0,3})(?P<key_name>"
                    + pattern
                    + r"\b)(?P=mark)(?P<link>[:=\s]{1,3})"
                    + r"(?P<vmark>['\"\\]{0,3})(.+?)(?P=vmark)(?P<end>[,\s]?)"
                )
                msg = re.sub(match_re, rep_re, msg, flags=re.I | re.M)
            return msg
        return msg
