# SPDX-License-Identifier: BSD-3-Clause
from . import exceptions as e
from . import urls
from . import http
from . import utils


def create_template(
    token: str,
    name: str = "",
    active: bool = True,
    frequnecy="daily",
    template: str = "arxiv",
    classes=None,
    data: str = "",
):
    raise NotImplementedError


def create_query(
    token: str,
    name: str = "",
    qid: str = "",
    active: bool = True,
    frequnecy="daily",
    data: str = "",
):
    raise NotImplementedError


def delete(token: str, myads_id: str):
    url = urls.make_url(urls.urls["notification"]["get"], myads_id)
    r = http.delete(token, url)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response


def edit():
    raise NotImplementedError


def query(token: str, myads_id: str):
    url = urls.make_url(urls.urls["notification"]["get"], myads_id)
    r = http.get(token, url, {}, json=False)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response


def view_all(token: str):

    url = urls.make_url(urls.urls["notification"]["edit"])
    r = http.get(token, url, {}, json=False)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response


def view(token: str, myads_id: str):
    url = urls.make_url(urls.urls["notification"]["edit"], myads_id)
    r = http.get(token, url, {}, json=False)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response
