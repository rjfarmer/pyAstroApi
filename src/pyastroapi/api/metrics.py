# SPDX-License-Identifier: BSD-3-Clause

from . import exceptions as e
from . import urls
from . import http
from . import utils

__all__ = [
    "detail",
    "metrics",
    "basic",
    "citations",
    "indicators",
    "histograms",
    "timeseries",
]


def detail(token: str, bibcode: str) -> http.HttpResponse:
    url = urls.make_url(urls.urls["metrics"]["detail"])
    r = http.post_bibcodes(token, url, bibcode)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response


def metrics(token: str, bibcode: str):
    url = urls.make_url(urls.urls["metrics"]["metrics"], bibcode)

    r = http.get(token, url)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response


def _metric(token: str, bibcode: str, format: str) -> str:

    url = urls.make_url(urls.urls["metrics"]["metrics"])
    payload = {"bibcodes": utils.ensure_list(bibcode), "types": [format]}
    r = http.post(token, url, payload)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response


def basic(token: str, bibcode: str) -> str:
    return _metric(token, bibcode, "basic")


def citations(token: str, bibcode: str) -> str:
    return _metric(token, bibcode, "citations")


def indicators(token: str, bibcode: str) -> str:
    return _metric(token, bibcode, "indicators")


def histograms(token: str, bibcode: str) -> str:
    return _metric(token, bibcode, "histograms")


def timeseries(token: str, bibcode: str) -> str:
    return _metric(token, bibcode, "timeseries")
