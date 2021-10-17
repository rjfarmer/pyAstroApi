# SPDX-License-Identifier: BSD-3-Clause

import typing as t

from . import exceptions as e
from . import urls
from . import http
from . import utils


def list_all(token: str):

    url = urls.make_url(urls.urls['libraries']['view'])

    data = http.get(url, token, {})

    if data.status != 200:
        if data.status == 400:
            raise e.NoADSAccount()
        else:
            raise e.AdsApiError('Unknown error code {}'.format(data.status))

    return data.response


def get_permissions(lib: str, token: str):
    url = urls.make_url(urls.urls['libraries']['permission'], lib)

    data = http.get(url, token, {})

    if data.status != 200:
        if data.status == 400:
            raise e.MalformedRequest
        elif data.status == 403:
            raise e.InsufficentPermisions
        else:
            raise e.AdsApiError('Unknown error code {}'.format(data.status))

    return data.response


def get(lib: str, token: str):
    start = 0
    count = 0
    while True:
        url = urls.make_url(urls.urls['libraries']['view'], lib, '?start='+str(start)+'&rows=20')

        data = http.get(url, token, {})

        if data.status != 200:
            raise e.AdsApiError('Unknown error code {}'.format(data.status))

        total_num = int(data.response['metadata']['num_documents'])

        count += len(data.response['documents'])

        yield from data.response['documents']

        if count == total_num:
            break
        else:
            start = count-1


def update_metadata(lib: str, token: str,
                    name: t.Optional[str]=None, description: t.Optional[str]=None, 
                    public: t.Optional[bool]=None):

    params = {}
    if name is not None:
        params['name'] = name
    if description is not None:
        params['description'] = description
    if public is not None:
        params['public'] = 'false'
        if public:
            params['public'] = 'true'

    url = urls.make_url(urls.urls['libraries']['change'], lib)

    data = http.put(url, token, params)

    if data.status != 200:
        if data.status == 400:
            raise e.MalformedRequest
        elif data.status == 403:
            raise e.InsufficentPermisions
        elif data.status == 409:
            raise e.LibraryAllreadyExists
        elif data.status == 410:
            raise e.LibraryDoesNotExist
        else:
            raise e.AdsApiError('Unknown error code {}'.format(data.status))


def transfer(lib: str, token: str, email: str):
    url = urls.make_url(urls.urls['libraries']['transfer'], lib)

    data = http.post(url, token, {'email': email})

    if data.status != 200:
        if data.status == 400:
            raise e.MalformedRequest
        elif data.status == 403:
            raise e.InsufficentPermisions
        elif data.status == 404:
            raise e.NoADSAccount
        else:
            raise e.AdsApiError('Unknown error code {}'.format(data.status))


def new(token: str, name: t.Optional[str]=None, description: t.Optional[str]=None, 
        public: t.Optional[bool]=None, bibcode: t.Optional[str]=None):

    params = {}
    if name is not None:
        params['name'] = name
    if description is not None:
        params['description'] = description
    if public is not None:
        params['public'] = 'false'
        if public:
            params['public'] = 'true'
    if bibcode is not None:
        params['bibcode'] = utils.ensure_list(bibcode)

    url = urls.make_url(urls.urls['libraries']['view'])

    data = http.post(url, token, params)

    if data.status != 200:
        if data.status == 400:
            raise e.MalformedRequest
        elif data.status == 409:
            raise e.LibraryAllreadyExists
        else:
            raise e.AdsApiError('Unknown error code {}'.format(data.status))


def delete(lib: str, token: str):
    url = urls.make_url(urls.urls['libraries']['change'], lib)

    data = http.delete(url, token)

    if data.status != 200:
        if data.status == 400:
            raise e.MalformedRequest
        elif data.status == 403:
            raise e.InsufficentPermisions
        elif data.status == 410:
            raise e.LibraryDoesNotExist
        else:
            raise e.AdsApiError('Unknown error code {}'.format(data.status))


def add(lib: str, bibcode: str, token: str):
    url = urls.make_url(urls.urls['libraries']['change'], lib)

    bibs = utils.ensure_list(bibcode)

    data = http.post(url, token, {
        'action': 'add',
        'bibcode': bibs
    })

    if data.status != 200:
        if data.status == 400:
            raise e.MalformedRequest
        elif data.status == 403:
            raise e.InsufficentPermisions
        else:
            raise e.AdsApiError('Unknown error code {}'.format(data.status))

    if len(bibs) != data.response['number_added']:
        raise e.AdsApiError('Bad number of bibcodes added tried {} got {}'.format(len(bibs), data.response['number_added']))


def remove(lib: str, bibcode: str, token: str):
    url = urls.make_url(urls.urls['libraries']['change'], lib)

    bibs = utils.ensure_list(bibcode)
    data = http.post(url, token, {
        'action': 'remove',
        'bibcode': bibs
    })

    if data.status != 200:
        if data.status == 400:
            raise e.MalformedRequest
        elif data.status == 403:
            raise e.InsufficentPermisions
        else:
            raise e.AdsApiError('Unknown error code {}'.format(data.status))

    if len(bibs) != data.response['number_added']:
        raise e.AdsApiError('Bad number of bibcodes removed tried {} got {}'.format(len(bibs), data.response['number_added']))
