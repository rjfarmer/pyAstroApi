# SPDX-License-Identifier: BSD-3-Clause

from . import exceptions as e
from . import urls
from . import http
from . import utils
import typing as t


def search(token: str, bibcode: t.Union[str, t.List[str]]):

    url = urls.make_url(urls.urls["authors"]["search"])

    data = http.post_bibcodes(token, url, bibcode)

    return data.response["data"]
