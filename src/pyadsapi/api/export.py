# SPDX-License-Identifier: BSD-3-Clause

from . import exceptions as e
from . import urls
from . import http
import typing as t

_exportType = t.List[str]


def _export(token: str, bibcode: t.Union[str, t.List[str]], format: str):
    if isinstance(bibcode, list):
        url = urls.make_url(urls.urls["export"][format])
        payload = {"bibcode": bibcode}
        data = http.post(token, url, payload)

    else:
        url = urls.make_url(urls.urls["export"][format], bibcode)
        data = http.get(token, url, json=False)

    if data.status != 200:
        if data.status == 404:
            raise e.NoRecordsFound
        else:
            raise e.AdsApiError(f"Unknown error code {data.status}")

    if isinstance(bibcode, list):
        result = data.response["export"]
    else:
        result = data.response

    return result


def ads(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    r = _export(token, bibcode, "ads").split("\n\n\n")
    return [i for i in r if i]


def bibtexabs(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    r = _export(token, bibcode, "bibtexabs").split("\n\n")
    return [i for i in r if i]


def bibtex(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    r = _export(token, bibcode, "bibtex").split("\n\n")
    return [i for i in r if i]


def endnote(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    r = _export(token, bibcode, "endnote").split("\n\n\n")
    return [i for i in r if i]


def medlars(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    r = _export(token, bibcode, "medlars").split("\n\n\n")
    return [i for i in r if i]


def procite(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    r = _export(token, bibcode, "procite").split("\n\n\n")
    return [i for i in r if i]


def refworks(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    r = _export(token, bibcode, "refworks").split("\n\n\n")
    return [i for i in r if i]


def ris(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    r = _export(token, bibcode, "ris").split("\n\n\n")
    return [i for i in r if i]


def aastex(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    r = _export(token, bibcode, "aastex").split("\n")
    return [i for i in r if i]


def icarus(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    r = _export(token, bibcode, "icarus").split("\n")
    return [i for i in r if i]


def mnras(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    r = _export(token, bibcode, "mnras").split("\n")
    return [i for i in r if i]


def soph(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    r = _export(token, bibcode, "soph").split("\n")
    return [i for i in r if i]


def dcxml(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    return [_export(token, bibcode, "dcxml")]  # unsplitable


def refxml(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    return [_export(token, bibcode, "refxml")]  # unsplitable


def refabsxml(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    return [_export(token, bibcode, "refabsxml")]  # unsplitable


def rss(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    return [_export(token, bibcode, "rss")]  # unsplitable


def votable(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    return [_export(token, bibcode, "votable")]  # unsplitable


def ieee(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    r = _export(token, bibcode, "ieee").split("\n")
    return [i for i in r if i]
