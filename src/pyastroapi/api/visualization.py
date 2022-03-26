# SPDX-License-Identifier: BSD-3-Clause

from . import exceptions as e
from . import urls
from . import http
from . import utils


def author(token: str, bibcode: str) -> http.HttpResponseResponse_t:

    url = urls.make_url(urls.urls["visual"]["author"])
    payload = {"bibcodes": utils.ensure_list(bibcode)}
    data = http.post(token, url, payload)

    if data.status != 200:
        if data.status == 400:
            raise e.MalformedRequest
        elif data.status == 403:
            raise e.UnableToGetResults
        elif data.status == 404:
            raise e.NoRecordsFound
        else:
            raise e.AdsApiError(f"Unknown error code {data.status}")
    return data.response


def paper(token: str, bibcode: str) -> http.HttpResponseResponse_t:

    url = urls.make_url(urls.urls["visual"]["paper"])
    payload = {"bibcodes": utils.ensure_list(bibcode)}
    data = http.post(token, url, payload)

    if data.status != 200:
        if data.status == 400:
            raise e.MalformedRequest
        elif data.status == 403:
            raise e.UnableToGetResults
        elif data.status == 404:
            raise e.NoRecordsFound
        else:
            raise e.AdsApiError(f"Unknown error code {data.status}")
    return data.response


def word_cloud(token: str, query: str, rows: str = 50) -> http.HttpResponseResponse_t:
    raise NotImplementedError

    # url = urls.make_url(urls.urls["visual"]["word-cloud"])

    # payload = {
    #     "q": query,
    #     "rows": rows,
    #     "sort": "date desc, bibcode desc",
    # }

    # data = http.post(token, url, payload)

    # if data.status != 200:
    #     if data.status == 400:
    #         raise e.MalformedRequest
    #     elif data.status == 403:
    #         raise e.UnableToGetResults
    #     elif data.status == 404:
    #         raise e.NoRecordsFound
    #     else:
    #         raise e.AdsApiError(f"Unknown error code {data.status}")
    # return data.response
