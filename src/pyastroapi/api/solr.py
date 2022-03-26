# SPDX-License-Identifier: BSD-3-Clause

from . import exceptions as e
from . import urls
from . import http
from . import utils
from . import search
import typing as t


def query(token, object):
    url = urls.make_url(urls.urls["objects"]["solr"])
    data = http.post(token, url, data={"query": [f"object:{object}"]})
    return data.response["query"]


def simbad(token, identifiers):
    url = urls.make_url(urls.urls["objects"]["objects"])

    data = {"source": "SIMBAD", "identifiers": utils.ensure_list(identifiers)}

    r = http.post(token, url, data=data)
    return r.response


def objects(token, objects):
    url = urls.make_url(urls.urls["objects"]["objects"])

    data = {"source": "SIMBAD", "objects": utils.ensure_list(objects)}

    r = http.post(token, url, data=data)
    return r.response
