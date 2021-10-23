# SPDX-License-Identifier: BSD-3-Clause

import requests
import os
import typing as t
import pickle

from dataclasses import dataclass

from . import limits
from . import utils
from . import exceptions as e

_TEST_LOGGING = os.environ.get("ADS_TEST_LOG", False)

HttpResponseResponse_t = t.Union[str, t.Dict[t.Any, t.Any]]
Payload_t = t.Union[t.Dict[str, t.List[str]], t.Dict[str, str]]


@dataclass
class HttpResponse:
    response: HttpResponseResponse_t
    status: int


class _BearerAuth(requests.auth.AuthBase):
    def __init__(self, token: str) -> None:
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + str(self.token)
        return r


def get(url: str, token: str, data: Payload_t, json: bool = True) -> HttpResponse:
    r = requests.get(
        url,
        auth=_BearerAuth(token),
        params=data,
        hooks={"response": _log_http},
    )

    response_code = r.status_code

    limits.update_limits(r.headers)

    if json:
        return HttpResponse(r.json(), response_code)
    else:
        return HttpResponse(r.text, response_code)


def post(url: str, token: str, data: Payload_t, json: bool = True) -> HttpResponse:
    r = requests.post(
        url,
        auth=_BearerAuth(token),
        headers={"Content-Type": "application/json", "Accept": "application/json"},
        json=data,
        hooks={"response": _log_http},
    )

    response_code = r.status_code

    limits.update_limits(r.headers)

    if json:
        return HttpResponse(r.json(), response_code)
    else:
        return HttpResponse(r.text, response_code)


def put(url: str, token: str, data: Payload_t) -> HttpResponse:
    r = requests.put(
        url,
        auth=_BearerAuth(token),
        headers={"Content-Type": "application/json"},
        json=data,
        hooks={"response": _log_http},
    )

    response_code = r.status_code

    limits.update_limits(r.headers)

    return HttpResponse(r.json(), response_code)


def delete(url: str, token: str) -> HttpResponse:
    r = requests.delete(
        url,
        auth=_BearerAuth(token),
        hooks={"response": _log_http},
    )

    response_code = r.status_code

    limits.update_limits(r.headers)

    return HttpResponse("", response_code)


def post_bibcodes(
    url: str, bibcodes: t.Union[str, t.List[str]], token: str
) -> HttpResponse:
    data = {"bibcodes": utils.ensure_list(bibcodes)}

    return post(url, token, data)


def get_bibcodes(
    url: str, bibcodes: t.Union[str, t.List[str]], token: str
) -> HttpResponse:
    pass


def _log_http(r, *args, **kwargs):
    print("Here")
    if _TEST_LOGGING:
        with open("http.log", "a") as f:
            print(r.url, r.text, file=f)
    else:
        pass
