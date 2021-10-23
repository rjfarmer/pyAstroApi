# SPDX-License-Identifier: BSD-3-Clause

from . import exceptions as e
from . import urls
from . import http
from . import utils
import typing as t


def citations(bibcode: t.Union[str, t.List[str]], token: str) -> http.HttpResponse:
    url = urls.make_url(urls.urls["citations"]["helper"])
    return http.post_bibcodes(url, bibcode, token)
