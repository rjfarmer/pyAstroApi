# SPDX-License-Identifier: BSD-3-Clause
from . import exceptions as e
from . import urls
from . import http
from . import utils

import typing as t


def query(token: str, queryId: str):
    url = urls.make_url(urls.urls["stored"]["search"], queryId)
    r = http.get(token, url, {}, True)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response


def query2svg(token: str, queryId: str):
    url = urls.make_url(urls.urls["stored"]["query2svg"], queryId)
    r = http.get(token, url, {}, False)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response


def save(token: str, query: str, fields: str, limit: int = 200):
    url = urls.make_url(urls.urls["stored"]["search"])

    data = {
        "q": query,
        "fl": fields,
        "start": 0,
        "rows": limit,
        "sort": "citation_count",
        "fq": "{!bitset}",
    }

    r = http.post(token, url, data)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response


def save_bigquery(
    token: str, bibcodes: t.Union[str, t.List[str]], fields: str, limit: int = 200
):
    url = urls.make_url(urls.urls["stored"]["query"])

    data = {
        "fl": fields,
        "start": 0,
        "rows": limit,
        "sort": "citation_count",
        "fq": "{!bitset}",
        "bigquery": "bibcode\n" + "\n".join(utils.ensure_list(bibcodes)),
    }

    r = http.post(token, url, data)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response


def search(token: str, queryId: str):
    url = urls.make_url(urls.urls["stored"]["execute_query"], queryId)
    r = http.get(token, url, {}, True)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response["response"]
