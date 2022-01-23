# SPDX-License-Identifier: BSD-3-Clause

from . import exceptions as e
from . import urls
from . import http
from . import utils
import typing as t


def citations(token: str, bibcode: t.Union[str, t.List[str]]) -> http.HttpResponse:
    url = urls.make_url(urls.urls["citations"]["helper"])
    return http.post_bibcodes(token, url, bibcode)
