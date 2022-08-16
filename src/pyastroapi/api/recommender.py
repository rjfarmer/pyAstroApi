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

    data = {}
    data["abstract"] = abstract
    data["title"] = title
    data["author"] = author
    data["year"] = year
    data["doctype"] = doctype
    data["match_doctype"] = match_doctype
    data["mustmatch"] = must_match

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
        raise e.AdsApiError(r.response["error"])

    return r.response["bibcodes"]


def similar(
    token,
    sort="first_author",
    num_docs=20,
    top_n_reads=50,
    cutoff_days=7,
):
    return _recommend(token, "similar", sort, num_docs, top_n_reads, cutoff_days)


def trending(
    token,
    sort="first_author",
    num_docs=20,
    top_n_reads=50,
    cutoff_days=7,
):
    return _recommend(token, "trending", sort, num_docs, top_n_reads, cutoff_days)


def reviews(
    token,
    sort="first_author",
    num_docs=20,
    top_n_reads=50,
    cutoff_days=7,
):
    return _recommend(token, "reviews", sort, num_docs, top_n_reads, cutoff_days)


def useful(
    token,
    sort="first_author",
    num_docs=20,
    top_n_reads=50,
    cutoff_days=7,
):
    return _recommend(token, "useful", sort, num_docs, top_n_reads, cutoff_days)
