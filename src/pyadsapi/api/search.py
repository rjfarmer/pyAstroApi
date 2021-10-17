# SPDX-License-Identifier: BSD-3-Clause


import typing as t
from urllib.parse import urlencode, quote_plus


from . import exceptions as e
from . import urls
from . import http
from . import utils

_fields = '''abs abstract ack aff aff_id alternate_bibcode 
            alternative_title arXiv arxiv_class author 
            author_count
            bibcode bigroup bibstem body 
            citation_count copyright 
            data database pubdate doctype doi
            full
            grant
            identifier inst issue 
            keyword
            lang
            object orcid orcid_user orcid_other
            page property
            read_count
            title
            vizier volume
            year
        '''.split()

_short_fl = "abstract,author,bibcode,pubdate,title,pub"


def search(token: str, query: str="*:*", fields:str=_short_fl, fq:str='',) -> t.Generator:
    start = 0
    count = 0
    while True:
        terms = [
            '?q='+query,
            'fl='+fields,
            'fq='+fq,
            'start='+str(start)
        ]

        search_term = '&'.join(terms)

        url = urls.make_url(urls.urls['search']['search'], search_term)
        print(url)
        data = http.get(url, token, {})

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
                raise e.AdsApiError('Unknown error code {}'.format(data.status))

        total_num = int(data.response['response']['numFound'])

        count += len(data.response['response']['docs'])

        yield from data.response['response']['docs']

        if count == total_num:
            break
        else:
            start = count-1


def bigquery(bibcodes: str, token: str):
    pass
