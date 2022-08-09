# SPDX-License-Identifier: BSD-3-Clause

from . import exceptions as e
from . import urls
from . import http
import typing as t

__all__ = ["search"]


def search(token: str, bibcode: t.Union[str, t.List[str]]):
    """Create an author-affiliations report.

    https://ui.adsabs.harvard.edu/help/api/api-docs.html#tag--author-affiliation

    Args:
        token (str): ADSABS token
        bibcode (t.Union[str, t.List[str]]): Either a single bibcode or a list of bibcodes

    Returns:
        list[dicts] : List of dicts. Each entry contains the author and affiliation
    """

    url = urls.make_url(urls.urls["authors"]["search"])

    r = http.post_bibcodes(token, url, bibcode, False)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response["data"]
