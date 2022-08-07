# SPDX-License-Identifier: BSD-3-Clause

from . import exceptions as e
from . import urls
from . import http
from . import utils

__all__ = ["author", "paper", "word_cloud"]


def author(token: str, bibcode: str):

    url = urls.make_url(urls.urls["visual"]["author"])
    payload = {"bibcodes": utils.ensure_list(bibcode)}
    r = http.post(token, url, payload)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response


def paper(token: str, bibcode: str):

    url = urls.make_url(urls.urls["visual"]["paper"])
    payload = {"bibcodes": utils.ensure_list(bibcode)}
    r = http.post(token, url, payload)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response


def word_cloud(token: str, query: str, rows: str = 50):
    url = urls.make_url(urls.urls["visual"]["word-cloud"])

    payload = {
        "q": [query],
        "rows": [rows],
        "sort": ["date desc, bibcode desc"],
    }

    r = http.post(token, url, payload)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response
