# SPDX-License-Identifier: BSD-3-Clause
from . import exceptions as e
from . import urls
from . import http
from . import utils


def query(token: str, queryId: str):
    url = urls.make_url(urls.urls["stored"]["search"], queryId)
    r = http.get(token, url, {}, False)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response


def query2svg(token: str, queryId: str):
    url = urls.make_url(urls.urls["stored"]["query2svg"], queryId)
    r = http.get(token, url, {}, False)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response


def save():
    raise NotImplementedError


def search(token: str, queryId: str):
    url = urls.make_url(urls.urls["stored"]["execute_query"], queryId)
    r = http.get(token, url, {}, False)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response
