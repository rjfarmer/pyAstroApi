# SPDX-License-Identifier: BSD-3-Clause
from . import exceptions as e
from . import urls
from . import http
from . import utils

__all__ = ["resolve"]


def resolve(token, reference):
    url = urls.make_url(urls.urls["ref"]["text"])

    data = {"reference": utils.ensure_list(reference)}

    r = http.post(token, url, data=data)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response["resolved"]
