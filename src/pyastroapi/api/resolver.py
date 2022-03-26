# SPDX-License-Identifier: BSD-3-Clause

from . import exceptions as e
from . import urls
from . import http


def resolve(token: str, bibcode: str) -> http.HttpResponseResponse_t:

    if isinstance(bibcode, list):
        raise TypeError("One bibcode at a time")

    url = urls.make_url(urls.urls["resolve"]["search"], bibcode)

    data = http.get(token, url)

    if data.status != 200:
        if data.status == 400:
            raise e.MalformedRequest
        elif data.status == 404:
            raise e.NoRecordsFound
        else:
            raise e.AdsApiError("Unknown error code {}".format(data.status))

    return data.response


def _get(token: str, bibcode: str, format: str) -> str:
    url = urls.make_url(urls.urls["resolve"]["search"], bibcode, format)

    data = http.get(token, url)

    if data.status != 200:
        if data.status == 403:
            raise e.UnableToGetResults
        if data.status == 404:
            raise e.NoRecordsFound
        elif data.status == 500:
            raise e.MetricsBlewUp
        else:
            raise e.AdsApiError("Unknown error code {}".format(data.status))

    return data.response


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
