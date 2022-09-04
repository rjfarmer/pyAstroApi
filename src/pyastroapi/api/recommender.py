# SPDX-License-Identifier: BSD-3-Clause
from . import exceptions as e
from . import urls
from . import http

import typing as t

__all__ = ["matchdoc", "similar", "trending", "reviews", "useful"]


def matchdoc(
    token: str,
    abstract: str = "",
    title: str = "",
    author: str = "",
    year: int = "",
    doctype: str = "article",
    match_doctype: t.List[str] = ["article"],
    must_match=True,
):
    url = urls.make_url(urls.urls["oracle"]["match"])

    data = {
        "abstract": abstract,
        "title": title,
        "author": author,
        "year": year,
        "doctype": doctype,
        "match_doctype": match_doctype,
        "mustmatch": must_match,
    }

    r = http.post(token, url, data=data, json=True)

    print(r)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response["match"]


def _recommend(
    token,
    function="similar",
    sort="first_author",
    num_docs=20,
    top_n_reads=50,
    cutoff_days=7,
):
    url = urls.make_url(urls.urls["oracle"]["read"])

    data = {
        "function": function,
        "sort": sort,
        "num_docs": num_docs,
        "top_n_reads": top_n_reads,
        "cutoff_days": cutoff_days,
    }

    r = http.post(token, url, data=data, json=True)

    if r.status != 200:
        if r.response["error"] == "no result from solr with status code=200":
            # Skip as things worked but theres no results
            # https://github.com/adsabs/oracle_service/issues/45
            return []
        else:
            raise e.AdsApiError(r.response["error"])

    return r.response["bibcodes"]


def similar(
    token,
    sort="first_author",
    num_docs=20,
    top_n_reads=50,
    cutoff_days=7,
):
    """Find papers similar to what the user reads

    Note for this to work you must be "active" that is logged in ADS, and in the past 90
    days active for at least 5 days.

    https://github.com/adsabs/oracle_service/issues/45#issuecomment-1235830947

    Args:
        token (_type_): ADS token
        sort (str, optional): Sort order, note this does not take a direction. Defaults to "first_author".
        num_docs (int, optional): Maximum number of docs to return. Defaults to 20.
        top_n_reads (int, optional): Number of records to use. Defaults to 50.
        cutoff_days (int, optional): Days back to use for recommedations. Defaults to 7.

    Returns:
        _type_: _description_
    """
    return _recommend(token, "similar", sort, num_docs, top_n_reads, cutoff_days)


def trending(
    token,
    sort="first_author",
    num_docs=20,
    top_n_reads=50,
    cutoff_days=7,
):
    """Find trending papers based on what the user reads

    Note for this to work you must be "active" that is logged in ADS, and in the past 90
    days active for at least 5 days.

    https://github.com/adsabs/oracle_service/issues/45#issuecomment-1235830947

    Args:
        token (_type_): ADS token
        sort (str, optional): Sort order, note this does not take a direction. Defaults to "first_author".
        num_docs (int, optional): Maximum number of docs to return. Defaults to 20.
        top_n_reads (int, optional): Number of records to use. Defaults to 50.
        cutoff_days (int, optional): Days back to use for recommedations. Defaults to 7.

    Returns:
        _type_: _description_
    """
    return _recommend(token, "trending", sort, num_docs, top_n_reads, cutoff_days)


def reviews(
    token,
    sort="first_author",
    num_docs=20,
    top_n_reads=50,
    cutoff_days=7,
):
    """Find reviews based on what the user reads

    Note for this to work you must be "active" that is logged in ADS, and in the past 90
    days active for at least 5 days.

    https://github.com/adsabs/oracle_service/issues/45#issuecomment-1235830947

    Args:
        token (_type_): ADS token
        sort (str, optional): Sort order, note this does not take a direction. Defaults to "first_author".
        num_docs (int, optional): Maximum number of docs to return. Defaults to 20.
        top_n_reads (int, optional): Number of records to use. Defaults to 50.
        cutoff_days (int, optional): Days back to use for recommedations. Defaults to 7.

    Returns:
        _type_: _description_
    """
    return _recommend(token, "reviews", sort, num_docs, top_n_reads, cutoff_days)


def useful(
    token,
    sort="first_author",
    num_docs=20,
    top_n_reads=50,
    cutoff_days=7,
):
    """Find "usefull" papers based on what the user reads

    Note for this to work you must be "active" that is logged in ADS, and in the past 90
    days active for at least 5 days.

    https://github.com/adsabs/oracle_service/issues/45#issuecomment-1235830947

    Args:
        token (_type_): ADS token
        sort (str, optional): Sort order, note this does not take a direction. Defaults to "first_author".
        num_docs (int, optional): Maximum number of docs to return. Defaults to 20.
        top_n_reads (int, optional): Number of records to use. Defaults to 50.
        cutoff_days (int, optional): Days back to use for recommedations. Defaults to 7.

    Returns:
        _type_: _description_
    """
    return _recommend(token, "useful", sort, num_docs, top_n_reads, cutoff_days)
