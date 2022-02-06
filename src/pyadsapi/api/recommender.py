# SPDX-License-Identifier: BSD-3-Clause
from . import exceptions as e
from . import urls
from . import http
from . import utils
from . import search
import typing as t


def matchdoc(token, metadata):
    raise NotImplementedError


def recommend(
    token,
    function="similiar",
    sort="first_author desc",
    num_docs=20,
    top_n_reads=50,
    cuttoff_days=7,
):
    url = urls.make_url(urls.urls["oracle"]["read"])

    data = {
        "function": function,
        "sort": sort,
        "num_docs": num_docs,
        "top_n_reads": top_n_reads,
        "cuttoff_days": cuttoff_days,
    }

    r = http.post(token, url, data=data)

    return r
