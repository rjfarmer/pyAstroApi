# SPDX-License-Identifier: BSD-3-Clause

from . import exceptions as e
from . import urls
from . import http
from . import utils
import typing as t

_exportType = t.List[str]

__all__ = [
    "ads",
    "bibtexabs",
    "bibtex",
    "endnote",
    "medlars",
    "procite",
    "refworks",
    "ris",
    "aastex",
    "icarus",
    "mnras",
    "soph",
    "dcxml",
    "refxml",
    "refabsxml",
    "rss",
    "votable",
    "ieee",
    "csl",
    "custom",
]


def _export(token: str, bibcode: t.Union[str, t.List[str]], format: str) -> str:
    """General method for exporting a reference

    Users should not call this directly.



    Args:
        token (str): ADSABS token
        bibcode (t.Union[str, t.List[str]]): Either a single bibcode or a list of bibcodes
        format (str): Requested export format

    Raises:
        e.NoRecordsFound: _description_
        e.AdsApiError: _description_

    Returns:
        str: Export data
    """
    url = urls.make_url(urls.urls["export"][format])
    data = {"bibcode": utils.ensure_list(bibcode)}
    r = http.post(token, url, data)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response["export"]


def ads(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    """Get the ADS format

    https://ui.adsabs.harvard.edu/help/api/api-docs.html#get-/export/ads/-bibcode-

    Args:
        token (str): ADSABS token
        bibcode (t.Union[str, t.List[str]]): Either a single bibcode or a list of bibcodes

    Returns:
        _exportType: Export data
    """
    r = _export(token, bibcode, "ads").split("\n\n\n")
    return [i for i in r if i]


def bibtexabs(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    """Get the Bibtex + abstract export

    https://ui.adsabs.harvard.edu/help/api/api-docs.html#get-/export/bibtexabs/-bibcode-

    Args:
        token (str): ADSABS token
        bibcode (t.Union[str, t.List[str]]): Either a single bibcode or a list of bibcodes

    Returns:
        _exportType: Export data
    """
    r = _export(token, bibcode, "bibtexabs").split("\n\n")
    return [i for i in r if i]


def bibtex(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    """Get the bibtex

    https://ui.adsabs.harvard.edu/help/api/api-docs.html#get-/export/bibtex/-bibcode-

    Args:
        token (str): ADSABS token
        bibcode (t.Union[str, t.List[str]]): Either a single bibcode or a list of bibcodes

    Returns:
        _exportType: Export data
    """
    r = _export(token, bibcode, "bibtex").split("\n\n")
    return [i for i in r if i]


def endnote(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    """Get the Endnote format

    https://ui.adsabs.harvard.edu/help/api/api-docs.html#get-/export/endnote/-bibcode-

    Args:
        token (str): ADSABS token
        bibcode (t.Union[str, t.List[str]]): Either a single bibcode or a list of bibcodes

    Returns:
        _exportType: Export data
    """
    r = _export(token, bibcode, "endnote").split("\n\n\n")
    return [i for i in r if i]


def medlars(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    """Get the MEDLARS format

    https://ui.adsabs.harvard.edu/help/api/api-docs.html#get-/export/medlars/-bibcode-

    Args:
        token (str): ADSABS token
        bibcode (t.Union[str, t.List[str]]): Either a single bibcode or a list of bibcodes

    Returns:
        _exportType: Export data
    """
    r = _export(token, bibcode, "medlars").split("\n\n\n")
    return [i for i in r if i]


def procite(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    """Get the Procite format

    https://ui.adsabs.harvard.edu/help/api/api-docs.html#get-/export/procite/-bibcode-

    Args:
        token (str): ADSABS token
        bibcode (t.Union[str, t.List[str]]): Either a single bibcode or a list of bibcodes

    Returns:
        _exportType: Export data
    """
    r = _export(token, bibcode, "procite").split("\n\n\n")
    return [i for i in r if i]


def refworks(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    """Get the Refworks format

    https://ui.adsabs.harvard.edu/help/api/api-docs.html#get-/export/refworks/-bibcode-

    Args:
        token (str): ADSABS token
        bibcode (t.Union[str, t.List[str]]): Either a single bibcode or a list of bibcodes

    Returns:
        _exportType: Export data
    """
    r = _export(token, bibcode, "refworks").split("\n\n\n")
    return [i for i in r if i]


def ris(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    """Get the RIS format

    https://ui.adsabs.harvard.edu/help/api/api-docs.html#get-/export/ris/-bibcode-

    Args:
        token (str): ADSABS token
        bibcode (t.Union[str, t.List[str]]): Either a single bibcode or a list of bibcodes

    Returns:
        _exportType: Export data
    """
    r = _export(token, bibcode, "ris").split("\n\n\n")
    return [i for i in r if i]


def aastex(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    """Get the AASTeX format

    https://ui.adsabs.harvard.edu/help/api/api-docs.html#get-/export/aastex/-bibcode-

    Args:
        token (str): ADSABS token
        bibcode (t.Union[str, t.List[str]]): Either a single bibcode or a list of bibcodes

    Returns:
        _exportType: Export data
    """
    r = _export(token, bibcode, "aastex").split("\n")
    return [i for i in r if i]


def icarus(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    """Get the Icarus format

    https://ui.adsabs.harvard.edu/help/api/api-docs.html#get-/export/icarus/-bibcode-

    Args:
        token (str): ADSABS token
        bibcode (t.Union[str, t.List[str]]): Either a single bibcode or a list of bibcodes

    Returns:
        _exportType: Export data
    """
    r = _export(token, bibcode, "icarus").split("\n")
    return [i for i in r if i]


def mnras(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    """Get the MNRAS  format

    https://ui.adsabs.harvard.edu/help/api/api-docs.html#get-/export/mnras/-bibcode-

    Args:
        token (str): ADSABS token
        bibcode (t.Union[str, t.List[str]]): Either a single bibcode or a list of bibcodes

    Returns:
        _exportType: Export data
    """
    r = _export(token, bibcode, "mnras").split("\n")
    return [i for i in r if i]


def soph(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    """Get the SoPh format

    https://ui.adsabs.harvard.edu/help/api/api-docs.html#get-/export/soph/-bibcode-

    Args:
        token (str): ADSABS token
        bibcode (t.Union[str, t.List[str]]): Either a single bibcode or a list of bibcodes

    Returns:
        _exportType: Export data
    """
    r = _export(token, bibcode, "soph").split("\n")
    return [i for i in r if i]


def dcxml(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    """Get the Dublin Core (DC) XML format

    https://ui.adsabs.harvard.edu/help/api/api-docs.html#get-/export/dcxml/-bibcode-

    Args:
        token (str): ADSABS token
        bibcode (t.Union[str, t.List[str]]): Either a single bibcode or a list of bibcodes

    Returns:
        _exportType: Export data
    """
    return [_export(token, bibcode, "dcxml")]  # unsplitable


def refxml(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    """Get the REF-XML format

    https://ui.adsabs.harvard.edu/help/api/api-docs.html#get-/export/refxml/-bibcode-

    Args:
        token (str): ADSABS token
        bibcode (t.Union[str, t.List[str]]): Either a single bibcode or a list of bibcodes

    Returns:
        _exportType: Export data
    """
    return [_export(token, bibcode, "refxml")]  # unsplitable


def refabsxml(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    """Get the REFABS  XML format

    https://ui.adsabs.harvard.edu/help/api/api-docs.html#get-/export/refabsxml/-bibcode-

    Args:
        token (str): ADSABS token
        bibcode (t.Union[str, t.List[str]]): Either a single bibcode or a list of bibcodes

    Returns:
        _exportType: Export data
    """
    return [_export(token, bibcode, "refabsxml")]  # unsplitable


def rss(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    """Get the RSS format

    https://ui.adsabs.harvard.edu/help/api/api-docs.html#get-/export/rss/-bibcode-

    Args:
        token (str): ADSABS token
        bibcode (t.Union[str, t.List[str]]): Either a single bibcode or a list of bibcodes

    Returns:
        _exportType: Export data
    """
    return [_export(token, bibcode, "rss")]  # unsplitable


def votable(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    """Get the VOTables format

    https://ui.adsabs.harvard.edu/help/api/api-docs.html#get-/export/votable/-bibcode-

    Args:
        token (str): ADSABS token
        bibcode (t.Union[str, t.List[str]]): Either a single bibcode or a list of bibcodes

    Returns:
        _exportType: Export data
    """
    return [_export(token, bibcode, "votable")]  # unsplitable


def ieee(token: str, bibcode: t.Union[str, t.List[str]]) -> _exportType:
    """Get the IEEE format

    https://ui.adsabs.harvard.edu/help/api/api-docs.html#get-/export/ieee/-bibcode-

    Args:
        token (str): ADSABS token
        bibcode (t.Union[str, t.List[str]]): Either a single bibcode or a list of bibcodes

    Returns:
        _exportType: Export data
    """
    r = _export(token, bibcode, "ieee").split("\n")
    return [i for i in r if i]


def csl(
    token: str,
    bibcodes: t.Union[str, t.List[str]],
    style: str = "aastex",
    format: str = "latex",
    journal: str = "aastex",
) -> _exportType:
    """Export in the given style format

    https://ui.adsabs.harvard.edu/help/api/api-docs.html#post-/export/csl

    Args:
        token (str): ADSABS token
        bibcode (t.Union[str, t.List[str]]): Either a single bibcode or a list of bibcodes
        style (str): Journal style to use must be one of aastex┃icarus┃mnras┃soph┃aspc┃apsj┃aasj┃ieee
        format (str): Output format must be one of unicode|html|latex
        journal (str): Format of journal name  must be one of aastex|abbev|full

    Returns:
        _exportType: Export data
    """

    _styles = ["aastex", "icarus", "mnras", "soph", "aspc", "apsj", "aasj", "ieee"]
    _formats = ["unicode", "html", "latex"]
    _journal = ["aastex", "abbev", "full"]

    if style not in _styles:
        raise ValueError(f"Bad style must be one of {_styles}")

    if format not in _formats:
        raise ValueError(f"Bad format must be one of {_formats}")

    if journal not in _journal:
        raise ValueError(f"Bad journal format must be one of {_journal}")

    format = _formats.index(format) + 1
    journal = _journal.index(journal) + 1

    data = {
        "bibcode": utils.ensure_list(bibcodes),
        "style": style,
        "format": format,
        "journalformat": journal,
        "sort": "first_author desc",
    }

    url = urls.make_url(urls.urls["export"]["csl"])

    r = http.post(token, url, data, json=True)

    if r.status != 200:
        if r.status == 404:
            raise e.NoRecordsFound(r.response["error"])
        else:
            raise e.AdsApiError(f"Unknown error code {r.status}")

    e = r.response["export"].split("\n")

    return [i for i in e if len(i)]


def custom(
    token: str,
    bibcodes: t.Union[str, t.List[str]],
    format: str,
) -> _exportType:
    """Export in a custom format

    https://ui.adsabs.harvard.edu/help/api/api-docs.html#post-/export/custom

    Args:
        token (str): ADSABS token
        bibcode (t.Union[str, t.List[str]]): Either a single bibcode or a list of bibcodes
        format (str) : Format code to use

    Returns:
        _exportType: Export data
    """
    data = {
        "bibcode": utils.ensure_list(bibcodes),
        "format": format,
    }

    url = urls.make_url(urls.urls["export"]["custom"])

    r = http.post(token, url, data, json=True)

    if r.status != 200:
        if r.status == 404:
            raise e.NoRecordsFound(r.response["error"])
        else:
            raise e.AdsApiError(f"Unknown error code {r.status}")

    e = r.response["export"].split("\n")

    return [i for i in e if len(i)]
