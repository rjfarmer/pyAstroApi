# SPDX-License-Identifier: BSD-3-Clause

from . import exceptions as e
from . import urls
from . import http
from . import utils

__all__ = ["query", "simbad", "objects"]


def query(token, object):
    url = urls.make_url(urls.urls["objects"]["solr"])
    r = http.post(token, url, data={"query": [f"object:{object}"]})

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response["query"]


def simbad(token, identifiers):
    url = urls.make_url(urls.urls["objects"]["objects"])

    data = {"source": "SIMBAD", "identifiers": utils.ensure_list(identifiers)}

    r = http.post(token, url, data=data)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response


def objects(token, objects):
    url = urls.make_url(urls.urls["objects"]["objects"])

    data = {"source": "SIMBAD", "objects": utils.ensure_list(objects)}

    r = http.post(token, url, data=data)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response
