# SPDX-License-Identifier: BSD-3-Clause


from argparse import ArgumentError
import typing as t
from urllib.parse import urlencode, quote_plus


from . import exceptions as e
from . import urls
from . import http
from . import utils

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
) -> t.Generator[t.Dict[t.Any, t.Any], None, None]:

    if fields is not None:
        for f in fields.split(","):
            if f and f not in _fields:
                raise ValueError(f"Field {f} not valid in search")
    else:
        fields = _short_fl

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

        search_term = "&".join(terms)

        url = urls.make_url(urls.urls["search"]["search"], search_term)
        # print(url)
        data = http.get(token, url)

        if data.status != 200:
            if data.status == 400:
                raise e.MalformedRequest
            elif data.status == 404:
                raise e.NoRecordsFound
            elif data.status == 499:
                raise e.ServerTooBusy
            elif data.status == 500:
                raise e.SeverError
            else:
                raise e.AdsApiError(f"Unknown error code {data.status}")

        total_num = int(data.response["response"]["numFound"])

        count += len(data.response["response"]["docs"])

        # print(count,total_num,start)

        yield from data.response["response"]["docs"]

        if count == total_num or count >= limit:
            break
        else:
            start = count - 1


def bigquery(token: str, bibcodes: t.List[str], limit: int = -1):
    # Broken for now
    terms = {
        "q": "*:*",
        "fl": "id,bibcode,title",
    }

    if limit > 0:
        terms["rows"] = str(limit)

    url = urls.make_url(urls.urls["search"]["bigquery"])

    bib = {"bibcodes": utils.ensure_list(bibcodes)}

    data = http.post(token, url, data=bib, params=terms, json=True)

    if data.status != 200:
        if data.status == 400:
            raise e.MalformedRequest
        elif data.status == 404:
            raise e.NoRecordsFound
        elif data.status == 499:
            raise e.ServerTooBusy
        elif data.status == 500:
            raise e.SeverError
        else:
            raise e.AdsApiError(f"Unknown error code {data.status}")

    return data
