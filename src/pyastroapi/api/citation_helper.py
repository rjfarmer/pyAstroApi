# SPDX-License-Identifier: BSD-3-Clause

from . import exceptions as e
from . import urls
from . import http
from . import utils
import typing as t


def citations(token: str, bibcode: t.List[str]):
    url = urls.make_url(urls.urls["citations"]["helper"])

    if not isinstance(bibcode, list):
        raise TypeError("Must pass a list of more than one bibcode")

    data = http.post_bibcodes(token, url, bibcode)

    return data.response
