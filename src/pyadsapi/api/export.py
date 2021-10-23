# SPDX-License-Identifier: BSD-3-Clause

from . import exceptions as e
from . import urls
from . import http
import typing as t


def _export(bibcode: t.Union[str, list], token: str, format: str) -> str:
    if isinstance(bibcode, list):
        url = urls.make_url(urls.urls["export"][format])
        payload = {"bibcode": bibcode}
        data = http.post(url, token, payload)

    else:
        url = urls.make_url(urls.urls["export"][format], bibcode)
        data = http.get(url, token, {}, json=False)

    if data.status != 200:
        if data.status == 404:
            raise e.NoRecordsFound
        else:
            raise e.AdsApiError("Unknown error code {}".format(data.status))

    result = {}
    if isinstance(bibcode, list):
        split = data.response["export"].split("\n\n\n")
        for i, j in zip(bibcode, split):
            result[i] = j
    else:
        result[bibcode] = data.response

    return result


def ads(bibcode: t.Union[str, t.List[str]], token: str) -> str:
    return _export(bibcode, token, "ads")


def bibtexabs(bibcode: t.Union[str, t.List[str]], token: str) -> str:
    return _export(bibcode, token, "bibtexabs")


def bibtex(bibcode: t.Union[str, t.List[str]], token: str) -> str:
    return _export(bibcode, token, "bibtex")


def endnote(bibcode: t.Union[str, t.List[str]], token: str) -> str:
    return _export(bibcode, token, "endnote")


def medlars(bibcode: t.Union[str, t.List[str]], token: str) -> str:
    return _export(bibcode, token, "medlars")


def procite(bibcode: t.Union[str, t.List[str]], token: str) -> str:
    return _export(bibcode, token, "procite")


def refworks(bibcode: t.Union[str, t.List[str]], token: str) -> str:
    return _export(bibcode, token, "refworks")


def ris(bibcode: t.Union[str, t.List[str]], token: str) -> str:
    return _export(bibcode, token, "ris")


def aastex(bibcode: t.Union[str, t.List[str]], token: str) -> str:
    return _export(bibcode, token, "aastex")


def icarus(bibcode: t.Union[str, t.List[str]], token: str) -> str:
    return _export(bibcode, token, "icarus")


def mnras(bibcode: t.Union[str, t.List[str]], token: str) -> str:
    return _export(bibcode, token, "mnras")


def soph(bibcode: t.Union[str, t.List[str]], token: str) -> str:
    return _export(bibcode, token, "soph")


def dcxml(bibcode: t.Union[str, t.List[str]], token: str) -> str:
    return _export(bibcode, token, "dcxml")


def refxml(bibcode: t.Union[str, t.List[str]], token: str) -> str:
    return _export(bibcode, token, "refxml")


def refabsxml(bibcode: t.Union[str, t.List[str]], token: str) -> str:
    return _export(bibcode, token, "refabsxml")


def rss(bibcode: t.Union[str, t.List[str]], token: str) -> str:
    return _export(bibcode, token, "rss")


def votable(bibcode: t.Union[str, t.List[str]], token: str) -> str:
    return _export(bibcode, token, "votable")


def ieee(bibcode: t.Union[str, t.List[str]], token: str) -> str:
    return _export(bibcode, token, "ieee")
