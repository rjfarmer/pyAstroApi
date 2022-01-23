# SPDX-License-Identifier: BSD-3-Clause

from . import exceptions as e
from . import urls
from . import http
import typing as t

_exportType = t.Dict[str, t.Any]


def _export(token: str, bibcode: t.Union[str, t.List[str]], format: str) -> _exportType:
    if isinstance(bibcode, list):
        url = urls.make_url(urls.urls["export"][format])
        payload = {"bibcode": bibcode}
        data = http.post(url, token, payload)

    else:
        url = urls.make_url(urls.urls["export"][format], bibcode)
        data = http.get(url, token, json=False)

    if data.status != 200:
        if data.status == 404:
            raise e.NoRecordsFound
        else:
            raise e.AdsApiError("Unknown error code {}".format(data.status))

    result = {}
    if isinstance(bibcode, list):
        split = data.response["export"].split("\n}\n\n")
        for i, j in zip(bibcode, split):
            result[i] = j + "}"
    else:
        result[bibcode] = data.response

    return result


def ads(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    return _export(token, bibcode, "ads")


def bibtexabs(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    return _export(token, bibcode, "bibtexabs")


def bibtex(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    return _export(token, bibcode, "bibtex")


def endnote(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    return _export(token, bibcode, "endnote")


def medlars(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    return _export(token, bibcode, "medlars")


def procite(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    return _export(token, bibcode, "procite")


def refworks(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    return _export(token, bibcode, "refworks")


def ris(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    return _export(token, bibcode, "ris")


def aastex(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    return _export(token, bibcode, "aastex")


def icarus(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    return _export(token, bibcode, "icarus")


def mnras(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    return _export(token, bibcode, "mnras")


def soph(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    return _export(token, bibcode, "soph")


def dcxml(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    return _export(token, bibcode, "dcxml")


def refxml(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    return _export(token, bibcode, "refxml")


def refabsxml(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    return _export(token, bibcode, "refabsxml")


def rss(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    return _export(token, bibcode, "rss")


def votable(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    return _export(token, bibcode, "votable")


def ieee(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    return _export(token, bibcode, "ieee")
