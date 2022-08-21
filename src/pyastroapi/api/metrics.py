# SPDX-License-Identifier: BSD-3-Clause

from . import exceptions as e
from . import urls
from . import http
from . import utils

import typing as t

__all__ = [
    "detail",
    "metrics",
    "basic",
    "citations",
    "indicators",
    "histograms",
    "timeseries",
]


def detail(token: str, bibcode: t.List[str]) -> t.Dict:
    """Provides basic, year-by-year metrics on a per-bibcode basis.

    https://ui.adsabs.harvard.edu/help/api/api-docs.html#tag--metrics

    Args:
        token (str): ADSABS token
        bibcode (t.List[str]): List of bibcodes

    Returns:
        dict: Metric data
    """
    url = urls.make_url(urls.urls["metrics"]["detail"])
    r = http.post_bibcodes(token, url, bibcode)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response


def metrics(token: str, bibcode: str) -> t.Dict:
    """Provides basic, year-by-year metrics on for a single bibcode

    https://ui.adsabs.harvard.edu/help/api/api-docs.html#tag--metrics
    Args:
        token (str): ADSABS token
        bibcode (str): Single bibcode

    Returns:
        dict: Metric data
    """
    url = urls.make_url(urls.urls["metrics"]["metrics"], bibcode)

    r = http.get(token, url)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response


def _metric(token: str, bibcode: t.List[str], format: str) -> t.Dict:

    url = urls.make_url(urls.urls["metrics"]["metrics"])
    payload = {"bibcodes": utils.ensure_list(bibcode), "types": [format]}
    r = http.post(token, url, payload)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response


def basic(token: str, bibcode: t.List[str]) -> t.Dict:
    """Publication and usage stats (all papers, and just refereed papers)

    Args:
        token (str): ADSABS token
        bibcode (t.List[str]): List of bibcodes

    Returns:
        dict: Metric data
    """
    return _metric(token, bibcode, "basic")


def citations(token: str, bibcode: t.List[str]) -> t.Dict:
    """citation stats

    Args:
        token (str): ADSABS token
        bibcode (t.List[str]): List of bibcodes

    Returns:
        dict: Metric data
    """
    return _metric(token, bibcode, "citations")


def indicators(token: str, bibcode: t.List[str]) -> t.Dict:
    """indicators, like the h-index, g-index, m-index, etc

    Args:
        token (str): ADSABS token
        bibcode (t.List[str]): List of bibcodes

    Returns:
        dict: Metric data
    """
    return _metric(token, bibcode, "indicators")


def histograms(token: str, bibcode: t.List[str]) -> t.Dict:
    """Publication, citation, reads and downloads histograms

    Args:
        token (str): ADSABS token
        bibcode (t.List[str]): List of bibcodes

    Returns:
        dict: Metric data
    """
    return _metric(token, bibcode, "histograms")


def timeseries(token: str, bibcode: t.List[str]) -> t.Dict:
    """time series for a set of indicators

    Args:
        token (str): ADSABS token
        bibcode (t.List[str]): List of bibcodes

    Returns:
        dict: Metric data
    """
    return _metric(token, bibcode, "timeseries")
