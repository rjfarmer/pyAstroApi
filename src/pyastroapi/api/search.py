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
    callback_start: t.Callable = None,  # Before search runs
    callback_num_results: t.Callable = None,  # Returns the number of rows found
    callback_search: t.Callable = None,  # Called with each result
    callback_end: t.Callable = None,  # Called once all results returned
    dbg: bool = False,
) -> t.Generator[t.Dict[t.Any, t.Any], None, None]:

    if fields is not None:
        for f in fields.split(","):
            if f and f not in _fields:
                raise ValueError(f"Field {f} not valid in search")
    else:
        fields = _short_fl

    split_f = fields.split(",")

    if callback_start is not None:
        callback_start(query, fields, fq, limit)

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

        if count == 0 and callback_num_results is not None:
            callback_num_results(total_num)

        if not len(data.response["response"]["docs"]):
            break

        count += len(data.response["response"]["docs"])

        for index, doc in enumerate(data.response["response"]["docs"]):
            for f in split_f:
                if f not in doc:
                    data.response["response"]["docs"][index][f] = None

        # print(count,total_num,start)
        if callback_search is None:
            yield from data.response["response"]["docs"]
        else:
            callback_search(data.response["response"]["docs"])

        if count >= total_num or (count >= limit and limit > 0):
            break
        else:
            start += count - 1

        if callback_end is not None:
            callback_end(query, fields, fq, limit, total_num)


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
