# SPDX-License-Identifier: BSD-3-Clause

from . import exceptions as e
from . import urls
from . import http
import typing as t


def search(token: str, bibcode: t.Union[str, t.List[str]]) -> http.HttpResponse:

    url = urls.make_url(urls.urls["authors"]["search"])

    return http.post_bibcodes(token, url, bibcode)
