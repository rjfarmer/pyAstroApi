# SPDX-License-Identifier: BSD-3-Clause

from . import exceptions as e
from . import urls
from . import http
import typing as t

__all__ = ["citations"]


def citations(token: str, bibcode: t.List[str]):
    """Given a set of bibcodes, suggest additional citations.

    https://ui.adsabs.harvard.edu/help/api/api-docs.html#tag--citation-helperc

    Args:
        token (str): ADSABS token
        bibcode (t.List[str]): List of bibcodes

    Raises:
        TypeError: Must pass a list of bibcodes

    Returns:
        _type_: _description_
    """

    url = urls.make_url(urls.urls["citations"]["helper"])

    if not isinstance(bibcode, list):
        raise TypeError("Must pass a list of more than one bibcode")

    r = http.post_bibcodes(token, url, bibcode, True)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response
