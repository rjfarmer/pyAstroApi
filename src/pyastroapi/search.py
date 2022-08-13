# # SPDX-License-Identifier: BSD-3-Clause

import datetime
import typing as t

import pyastroapi.api.search as _search
import pyastroapi.api.token as _token

__all__ = [
    "search",
    "first_author",
    "author_year",
    "orcid",
    "bibcode",
    "citations",
    "references",
    "astro_ph",
]


def search(query: str, limit: int = -1, fields: t.List[str] = None, dbg: bool = False):
    """Performs an ADS search

    Args:
        query (str): Search query
        limit (int, optional): Number of rows to limit to (-1 is no limit). Defaults to -1.
        fields (t.List[str], optional): ADS fields to return, if None returns a default set of fields.
        dbg (bool, optional): Debugging flag. Defaults to False.

    Returns:
        generator: Returns a generator where each element is a dict for each ADS record, with keys given by the fields
    """
    return _search.search(
        _token.get_token(), query=query, limit=limit, fields=fields, dbg=dbg
    )


def first_author(
    author: str, limit: int = -1, fields: t.List[str] = None, dbg: bool = False
):
    """Performs an ads search equivalent to: ^author

    Args:
        author (str): Author to search for
        limit (int, optional): Number of rows to limit to (-1 is no limit). Defaults to -1.
        fields (t.List[str], optional): ADS fields to return, if None returns a default set of fields.
        dbg (bool, optional): Debugging flag. Defaults to False.

    Returns:
        generator: Returns a generator where each element is a dict for each ADS record, with keys given by the fields
    """
    return search(query=f"^{author}", fields=fields)


def author_year(
    author, year, limit: int = -1, fields: t.List[str] = None, dbg: bool = False
):
    """Performs an ads search equivalent to: ^author year:year

    Args:
        author (str): Author to search for
        year (int): Year to limit to
        limit (int, optional): Number of rows to limit to (-1 is no limit). Defaults to -1.
        fields (t.List[str], optional): ADS fields to return, if None returns a default set of fields.
        dbg (bool, optional): Debugging flag. Defaults to False.

    Returns:
        generator: Returns a generator where each element is a dict for each ADS record, with keys given by the fields
    """
    return search(query=f"^{author} year:{year}", fields=fields)


def orcid(orcid: str, limit: int = -1, fields: t.List[str] = None, dbg: bool = False):
    """Performs an ads search equivalent to: orcid:orcid

    Args:
        orcid (str): ORCID
        limit (int, optional): Number of rows to limit to (-1 is no limit). Defaults to -1.
        fields (t.List[str], optional): ADS fields to return, if None returns a default set of fields.
        dbg (bool, optional): Debugging flag. Defaults to False.

    Returns:
        generator: Returns a generator where each element is a dict for each ADS record, with keys given by the fields
    """
    return search(query=f"orcid:{orcid}", fields=fields)


def bibcode(
    bibcode: str, limit: int = -1, fields: t.List[str] = None, dbg: bool = False
):
    """Searches for a given bibcode

    Args:
        bibcode (str): Bibcode
        limit (int, optional): Number of rows to limit to (-1 is no limit). Defaults to -1.
        fields (t.List[str], optional): ADS fields to return, if None returns a default set of fields.
        dbg (bool, optional): Debugging flag. Defaults to False.

    Returns:
        generator: Returns a generator where each element is a dict for each ADS record, with keys given by the fields
    """
    return search(query=f"bibcode:{bibcode}", fields=fields)


def citations(
    bibcode: str, limit: int = -1, fields: t.List[str] = None, dbg: bool = False
):
    """Gets citations to paper given by bibcode

    Args:
        bibcode (str): Bibcode
        limit (int, optional): Number of rows to limit to (-1 is no limit). Defaults to -1.
        fields (t.List[str], optional): ADS fields to return, if None returns a default set of fields.
        dbg (bool, optional): Debugging flag. Defaults to False.

    Returns:
        generator: Returns a generator where each element is a dict for each ADS record, with keys given by the fields
    """
    return search(query=f"citations({bibcode})", fields=fields)


def references(
    bibcode: str, limit: int = -1, fields: t.List[str] = None, dbg: bool = False
):
    """Get the papers referenced by paper given by bibcode

     Args:
        bibcode (str): Bibcode
        limit (int, optional): Number of rows to limit to (-1 is no limit). Defaults to -1.
        fields (t.List[str], optional): ADS fields to return, if None returns a default set of fields.
        dbg (bool, optional): Debugging flag. Defaults to False.

    Returns:
        generator: Returns a generator where each element is a dict for each ADS record, with keys given by the fields
    """
    return search(query=f"references({bibcode})", fields=fields)


def astro_ph(limit: int = -1, fields: t.List[str] = None, dbg: bool = False):
    """Gets the previous (working) days Arxiv postings

    Args:
        limit (int, optional): Number of rows to limit to (-1 is no limit). Defaults to -1.
        fields (t.List[str], optional): ADS fields to return, if None returns a default set of fields.
        dbg (bool, optional): Debugging flag. Defaults to False.

    Returns:
        generator: Returns a generator where each element is a dict for each ADS record, with keys given by the fields
    """
    day = datetime.datetime.today().weekday()

    if day <= 4:  # Monday to Friday get the last days arxiv:
        q = "[NOW-1DAYS TO *]"
    elif day == 5:  # Saturday
        q = "[NOW-2DAYS TO *]"
    elif day == 6:  # Sunday
        q = "[NOW-3DAYS TO *]"

    return search(f'arxiv_class:"astro-ph.*" entdate:{q}', limit, fields, dbg)
