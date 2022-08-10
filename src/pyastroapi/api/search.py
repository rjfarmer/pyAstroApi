# SPDX-License-Identifier: BSD-3-Clause

import typing as t

from . import exceptions as e
from . import urls
from . import http
from . import utils

__all__ = ["search", "bigquery"]

_fields = set(
    """abstract ack aff aff_id alternate_bibcode alternate_title arxiv_class author author_count author_norm 
    bibcode bibgroup bibstem 
    citation citation_count cite_read_boost classic_factor comment copyright 
    data database date doctype doi 
    eid entdate entry_date esources 
    facility first_author first_author_norm 
    grant grant_agencies grant_id 
    id identifier indexstamp inst isbn issn issue 
    keyword keyword_norm keyword_schema 
    lang links_data 
    nedid nedtype 
    orcid_pub orcid_other orcid_user 
    page page_count page_range property pub pub_raw pubdate pubnote 
    read_count reference 
    simbid 
    title 
    vizier volume
    year
    """.split()
)

_short_fl = "abstract,author,bibcode,pubdate,title,pub,year,citation_count,reference"


def search(
    token: str,
    query: str = "*:*",
    fields: str = None,
    fq: str = "",
    limit: int = -1,
    dbg: bool = False,
) -> t.Generator[t.Dict[t.Any, t.Any], None, None]:

    if fields is not None:
        for f in fields.split(","):
            if f and f not in _fields:
                raise ValueError(f"Field {f} not valid in search")
    else:
        fields = _short_fl

    split_f = fields.split(",")

    start = 0
    count = 0
    while True:
        terms = [
            f"?q={query}",
            f"fl={fields}",
            f"fq={fq}",
            f"start={start}",
        ]

        if limit > 0:
            terms.append(f"rows={limit}")
        else:
            terms.append(f"rows=50")

        search_term = "&".join(terms)

        url = urls.make_url(urls.urls["search"]["search"], search_term)

        if dbg:
            print(url)
        r = http.get(token, url)

        if r.status != 200:
            raise e.AdsApiError(r.response["error"])

        total_num = int(r.response["response"]["numFound"])

        if not len(r.response["response"]["docs"]):
            break

        count += len(r.response["response"]["docs"])

        for index, doc in enumerate(r.response["response"]["docs"]):
            for f in split_f:
                if f not in doc:
                    r.response["response"]["docs"][index][f] = None

        # print(count,total_num,start)
        yield from r.response["response"]["docs"]

        if count >= total_num or (count >= limit and limit > 0):
            break
        else:
            start += count - 1


def bigquery(token: str, bibcodes: t.List[str], limit: int = 10, q="*:*", fields=None):

    if fields is None:
        fields = "id,bibcode,title"

    terms = {"q": q, "fl": fields, "rows": limit}

    url = urls.make_url(urls.urls["search"]["bigquery"])

    r = http.bigquery_bibcodes(token, url, bibcodes=bibcodes, params=terms)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response["response"]
