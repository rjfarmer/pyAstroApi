# SPDX-License-Identifier: BSD-3-Clause
from . import exceptions as e
from . import urls
from . import http
from . import utils

import typing as t


def create_template(
    token: str,
    name: str = "",
    active: bool = True,
    stateful: bool = True,
    frequency: str = "daily",
    template: str = "arxiv",
    classes: t.List[str] = ["astro-ph"],
    data: str = "",
):

    url = urls.make_url(urls.urls["notification"]["edit"])

    data = {
        "type": "template",
        "name": name,
        "active": active,
        "stateful": stateful,
        "frequency": frequency,
        "classes": classes,
        "template": template,
    }

    r = http.post(token, url, data=data)

    if r.status != 200 and r.status != 204:
        try:
            error = r.response["error"]
        except TypeError:
            error = str(r.status)

        raise e.AdsApiError(error)

    return r.response


def create_query(
    token: str,
    name: str = "",
    active: bool = True,
    stateful: bool = True,
    frequency: str = "daily",
    qid: str = "",
    data: str = "",
):

    url = urls.make_url(urls.urls["notification"]["edit"])

    data = {
        "type": "query",
        "name": name,
        "active": active,
        "stateful": stateful,
        "frequency": frequency,
        "qid": qid,
        "data": data,
    }

    r = http.post(token, url, data=data)

    if r.status != 200 and r.status != 204:
        try:
            error = r.response["error"]
        except TypeError:
            error = str(r.status)

        raise e.AdsApiError(error)

    return r.response


def delete(token: str, myads_id: str):
    url = urls.make_url(urls.urls["notification"]["edit"], str(myads_id))
    r = http.delete(token, url)

    if r.status != 200 and r.status != 204:
        try:
            error = r.response["error"]
        except TypeError:
            error = str(r.status)

        raise e.AdsApiError(error)

    return r.response


def edit():
    raise NotImplementedError


def query(token: str, myads_id: str):
    url = urls.make_url(urls.urls["notification"]["get"], str(myads_id))
    r = http.get(token, url, {}, json=False)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response


def view_all(token: str):

    url = urls.make_url(urls.urls["notification"]["edit"])
    r = http.get(token, url, {}, json=True)

    if r.status != 200 and r.status != 204:
        try:
            error = r.response["error"]
        except TypeError:
            error = str(r.status)

        raise e.AdsApiError(error)

    return r.response


def view(token: str, myads_id: str):
    url = urls.make_url(urls.urls["notification"]["edit"], myads_id)
    r = http.get(token, url, {}, json=True)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response
