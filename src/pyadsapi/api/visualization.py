# SPDX-License-Identifier: BSD-3-Clause

from . import exceptions as e
from . import urls
from . import http
from . import utils


def author(bibcode: str, token: str) -> http.HttpResponseResponse_t:

    url = urls.make_url(urls.urls["visual"]["author"])
    payload = {"bibcodes": utils.ensure_list(bibcode)}
    data = http.post(url, token, payload)

    if data.status != 200:
        if data.status == 400:
            raise e.MalformedRequest
        elif data.status == 403:
            raise e.UnableToGetResults
        elif data.status == 404:
            raise e.NoRecordsFound
        else:
            raise e.AdsApiError("Unknown error code {}".format(data.status))
    return data.response


def paper(bibcode: str, token: str) -> http.HttpResponseResponse_t:

    url = urls.make_url(urls.urls["visual"]["paper"])
    payload = {"bibcodes": utils.ensure_list(bibcode)}
    data = http.post(url, token, payload)

    if data.status != 200:
        if data.status == 400:
            raise e.MalformedRequest
        elif data.status == 403:
            raise e.UnableToGetResults
        elif data.status == 404:
            raise e.NoRecordsFound
        else:
            raise e.AdsApiError("Unknown error code {}".format(data.status))
    return data.response


def word_cloud(query: str, rows: str, token: str) -> http.HttpResponseResponse_t:

    url = urls.make_url(urls.urls["visual"]["word-cloud"])

    payload = {
        "q": query,
        "rows": rows,
    }

    data = http.post(url, token, payload)

    if data.status != 200:
        if data.status == 400:
            raise e.MalformedRequest
        elif data.status == 403:
            raise e.UnableToGetResults
        elif data.status == 404:
            raise e.NoRecordsFound
        else:
            raise e.AdsApiError("Unknown error code {}".format(data.status))
    return data.response
