# SPDX-License-Identifier: BSD-3-Clause

from . import exceptions as e
from . import urls
from . import http
from . import utils


def detail(bibcode: str, token: str) -> http.HttpResponse:
    url = urls.make_url(urls.urls['metrics']['detail'])
    return http.post_bibcodes(url, bibcode, token)


def metrics(bibcode: str, token: str):
    url = urls.make_url(urls.urls['metrics']['metrics'], bibcode)

    data = http.get(url, token, {})

    if data.status != 200:
        if data.status == 400:
            raise e.MalformedRequest
        elif data.status == 403:
            raise e.UnableToGetResults
        elif data.status == 500:
            raise e.MetricsBlewUp
        else:
            raise e.AdsApiError('Unknown error code {}'.format(data.status))

    return data.response


def _metric(bibcode: str, token: str, format: str) -> str:

    url = urls.make_url(urls.urls['metrics']['metrics'])
    payload = {
        'bibcodes': utils.ensure_list(bibcode),
        'types': [format]
    }
    data = http.post(url, token, payload)

    if data.status != 200:
        if data.status == 403:
            raise e.UnableToGetResults
        elif data.status == 500:
            raise e.MetricsBlewUp
        else:
            raise e.AdsApiError('Unknown error code {}'.format(data.status))

    # if isinstance(bibcode, list):
    #     split = d['export'].split('\n\n\n')
    #     data = {}
    #     for i,j in zip(bibcode,split):
    #         data[i] = j
    # else:
    #     data = {}
    #     data[bibcode] = d

    return data.response


def basic(bibcode: str, token: str) -> str:
    return _metric(bibcode, token, 'basic')


def citations(bibcode: str, token: str) -> str:
    return _metric(bibcode, token, 'citations')


def indicators(bibcode: str, token: str) -> str:
    return _metric(bibcode, token, 'indicators')


def histograms(bibcode: str, token: str) -> str:
    return _metric(bibcode, token, 'histograms')


def timeseries(bibcode: str, token: str) -> str:
    return _metric(bibcode, token, 'timeseries')
