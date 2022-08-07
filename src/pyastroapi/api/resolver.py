# SPDX-License-Identifier: BSD-3-Clause

from . import exceptions as e
from . import urls
from . import http

__all__ = [
    "resolve",
    "abstract",
    "citations",
    "references",
    "coreads",
    "toc",
    "openurl",
    "metrics",
    "graphics",
    "data",
    "inspire",
    "esource",
    "librarycatalog",
    "presentation",
    "associated",
]


def resolve(token: str, bibcode: str):

    if isinstance(bibcode, list):
        raise TypeError("One bibcode at a time")

    url = urls.make_url(urls.urls["resolve"]["search"], bibcode)

    r = http.get(token, url)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response


def _get(token: str, bibcode: str, format: str) -> str:
    url = urls.make_url(urls.urls["resolve"]["search"], bibcode, format)

    r = http.get(token, url)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response


def abstract(token: str, bibcode: str) -> str:
    return _get(token, bibcode, "abstract")


def citations(token: str, bibcode: str) -> str:
    return _get(token, bibcode, "citations")


def references(token: str, bibcode: str) -> str:
    return _get(token, bibcode, "references")


def coreads(token: str, bibcode: str) -> str:
    return _get(token, bibcode, "coreads")


def toc(token: str, bibcode: str) -> str:
    return _get(token, bibcode, "toc")


def openurl(token: str, bibcode: str) -> str:
    return _get(token, bibcode, "openurl")


def metrics(token: str, bibcode: str) -> str:
    return _get(token, bibcode, "metrics")


def graphics(token: str, bibcode: str) -> str:
    return _get(token, bibcode, "graphics")


def data(token: str, bibcode: str) -> str:
    return _get(token, bibcode, "data")


def inspire(token: str, bibcode: str) -> str:
    return _get(token, bibcode, "inspire")


def esource(token: str, bibcode: str) -> str:
    return _get(token, bibcode, "esource")


def librarycatalog(token: str, bibcode: str) -> str:
    return _get(token, bibcode, "librarycatalog")


def presentation(token: str, bibcode: str) -> str:
    return _get(token, bibcode, "presentation")


def associated(token: str, bibcode: str) -> str:
    return _get(token, bibcode, "associated")
