# SPDX-License-Identifier: BSD-3-Clause

import typing as t

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
    return http.post_bibcodes(url, token, bibcode)


def metrics(token: str, bibcode: str):
    url = urls.make_url(urls.urls["metrics"]["metrics"], bibcode)

    data = http.get(token, url)

    if data.status != 200:
        if data.status == 400:
            raise e.MalformedRequest
        elif data.status == 403:
            raise e.UnableToGetResults
        elif data.status == 500:
            raise e.MetricsBlewUp
        else:
            raise e.AdsApiError("Unknown error code {}".format(data.status))

    return data.response


def _metric(token: str, bibcode: str, format: str) -> str:

    url = urls.make_url(urls.urls["metrics"]["metrics"])
    payload = {"bibcodes": utils.ensure_list(bibcode), "types": [format]}
    data = http.post(token, url, payload)

    if data.status != 200:
        if data.status == 403:
            raise e.UnableToGetResults
        elif data.status == 500:
            raise e.MetricsBlewUp
        else:
            raise e.AdsApiError("Unknown error code {}".format(data.status))

    return data.response


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
