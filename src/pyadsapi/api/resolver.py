# SPDX-License-Identifier: BSD-3-Clause

from . import exceptions as e
from . import urls
from . import http


def resolve(bibcode: str, token: str) -> http.HttpResponseResponse_t:
    url = urls.make_url(urls.urls["resolve"]["search"], bibcode)

    data = http.get(url, token)

    if data.status != 200:
        if data.status == 400:
            raise e.MalformedRequest
        elif data.status == 404:
            raise e.NoRecordsFound
        else:
            raise e.AdsApiError("Unknown error code {}".format(data.status))

    return data.response


def _get(bibcode: str, token: str, format: str) -> str:
    url = urls.make_url(urls.urls["resolve"]["search"], bibcode, format)

    data = http.get(url, token)

    if data.status != 200:
        if data.status == 403:
            raise e.UnableToGetResults
        if data.status == 404:
            raise e.NoRecordsFound
        elif data.status == 500:
            raise e.MetricsBlewUp
        else:
            raise e.AdsApiError("Unknown error code {}".format(data.status))

    return str(data.response)


def abstract(bibcode: str, token: str) -> str:
    return _get(bibcode, token, "abstract")


def citations(bibcode: str, token: str) -> str:
    return _get(bibcode, token, "citations")


def references(bibcode: str, token: str) -> str:
    return _get(bibcode, token, "references")


def coreads(bibcode: str, token: str) -> str:
    return _get(bibcode, token, "coreads")


def toc(bibcode: str, token: str) -> str:
    return _get(bibcode, token, "toc")


def openurl(bibcode: str, token: str) -> str:
    return _get(bibcode, token, "openurl")


def metrics(bibcode: str, token: str) -> str:
    return _get(bibcode, token, "metrics")


def graphics(bibcode: str, token: str) -> str:
    return _get(bibcode, token, "graphics")


def data(bibcode: str, token: str) -> str:
    return _get(bibcode, token, "data")


def inspire(bibcode: str, token: str) -> str:
    return _get(bibcode, token, "inspire")


def esource(bibcode: str, token: str) -> str:
    return _get(bibcode, token, "esource")


def librarycatalog(bibcode: str, token: str) -> str:
    return _get(bibcode, token, "librarycatalog")


def presentation(bibcode: str, token: str) -> str:
    return _get(bibcode, token, "presentation")


def associated(bibcode: str, token: str) -> str:
    return _get(bibcode, token, "associated")
