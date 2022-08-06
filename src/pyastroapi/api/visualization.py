# SPDX-License-Identifier: BSD-3-Clause

from . import exceptions as e
from . import urls
from . import http
from . import utils


def author(token: str, bibcode: str):

    url = urls.make_url(urls.urls["visual"]["author"])
    payload = {"bibcodes": utils.ensure_list(bibcode)}
    r = http.post(token, url, payload)

    if r.status != 200:
        if r.status == 400:
            raise e.MalformedRequest
        elif r.status == 403:
            raise e.UnableToGetResults
        elif r.status == 404:
            raise e.NoRecordsFound
        else:
            raise e.AdsApiError(f"Unknown error code {r.status}")
    return r.response


def paper(token: str, bibcode: str):

    url = urls.make_url(urls.urls["visual"]["paper"])
    payload = {"bibcodes": utils.ensure_list(bibcode)}
    r = http.post(token, url, payload)

    if r.status != 200:
        if r.status == 400:
            raise e.MalformedRequest
        elif r.status == 403:
            raise e.UnableToGetResults
        elif r.status == 404:
            raise e.NoRecordsFound
        else:
            raise e.AdsApiError(f"Unknown error code {r.status}")
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
        if r.status == 400:
            raise e.MalformedRequest
        elif r.status == 403:
            raise e.UnableToGetResults
        else:
            raise e.AdsApiError(f"Unknown error code {r.status}")
    return r.response
