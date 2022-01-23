# SPDX-License-Identifier: BSD-3-Clause

import requests
import os
import typing as t

from dataclasses import dataclass

from . import utils
from . import exceptions as e


class _BearerAuth(requests.auth.AuthBase):
    def __init__(self, token: str) -> None:
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + str(self.token)
        return r


HttpResponseResponse_t = t.Any

Payload_t = t.Union[
    t.Dict[str, t.List[str]],
    t.Dict[str, str],
    t.Dict[str, t.Sequence[str]],
    t.Dict[str, bool],
    t.Dict[str, _BearerAuth],
    None,
]


@dataclass
class ADSLimits:
    limit: int = -1
    remaining: int = -1
    reset: int = -1

    def __init__(self, header):
        try:
            self.limit = header["X-RateLimit-Limit"]
            self.remaining = header["X-RateLimit-Remaining"]
            self.reset = header["X-RateLimit-Reset"]
        except KeyError:
            pass


@dataclass
class HttpResponse:
    response: HttpResponseResponse_t
    status: int
    limits: ADSLimits


def get(
    token: str, url: str, data: Payload_t = None, json: bool = True
) -> HttpResponse:
    if data is None:
        data = {}  # type:ignore

    r = requests.get(
        url,
        auth=_BearerAuth(token),
        params=data,
    )

    response_code = r.status_code

    if json:
        return HttpResponse(r.json(), response_code, ADSLimits(r.headers))
    else:
        return HttpResponse(r.text, response_code, ADSLimits(r.headers))


def post(
    token: str,
    url: str,
    data: Payload_t = None,
    params: t.Any = None,
    json: bool = True,
) -> HttpResponse:

    args = {}  # type:ignore
    args["auth"] = _BearerAuth(token)

    if data is not None:
        args["json"] = data
        args["headers"] = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    if params is not None:
        args["params"] = params

    r = requests.post(url, **args)  # type:ignore

    response_code = r.status_code

    if json:
        return HttpResponse(r.json(), response_code, ADSLimits(r.headers))
    else:
        return HttpResponse(r.text, response_code, ADSLimits(r.headers))


def put(url: str, token: str, data: Payload_t) -> HttpResponse:
    r = requests.put(
        url,
        auth=_BearerAuth(token),
        headers={"Content-Type": "application/json"},
        json=data,
    )

    response_code = r.status_code

    return HttpResponse(r.json(), response_code, ADSLimits(r.headers))


def delete(token: str, url: str) -> HttpResponse:
    r = requests.delete(
        url,
        auth=_BearerAuth(token),
    )

    response_code = r.status_code

    return HttpResponse("", response_code, ADSLimits(r.headers))


def post_bibcodes(
    token: str, url: str, bibcodes: t.Union[str, t.List[str]]
) -> HttpResponse:
    data = {"bibcodes": utils.ensure_list(bibcodes)}

    return post(token, url, data)


def get_bibcodes(
    token: str, url: str, bibcodes: t.Union[str, t.List[str]]
) -> HttpResponse:
    pass
