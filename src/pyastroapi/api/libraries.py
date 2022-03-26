# SPDX-License-Identifier: BSD-3-Clause

import typing as t

from . import exceptions as e
from . import urls
from . import http
from . import utils


def list_all(token: str):

    url = urls.make_url(urls.urls["libraries"]["view"])

    data = http.get(token, url)

    if data.status != 200:
        if data.status == 400:
            raise e.NoADSAccount()
        else:
            raise e.AdsApiError(f"Unknown error code {data.status}")

    return data.response


def get_permissions(token: str, lib: str):
    url = urls.make_url(urls.urls["libraries"]["permission"], lib)

    data = http.get(token, url)

    if data.status != 200:
        if data.status == 400:
            raise e.MalformedRequest
        elif data.status == 403:
            raise e.InsufficentPermisions
        else:
            raise e.AdsApiError(f"Unknown error code {data.status}")

    return data.response


def get(token: str, lib: str):
    start = 0
    count = 0
    while True:
        url = urls.make_url(urls.urls["libraries"]["view"], lib, "?start=" + str(start))

        data = http.get(token, url)

        if data.status != 200:
            raise e.AdsApiError(f"Unknown error code {data.status}")

        total_num = int(data.response["metadata"]["num_documents"])

        if len(data.response["documents"]) == 0:
            # Total_num lies sometimes so track when we stop getting new papers
            break

        count += len(data.response["documents"])

        yield from data.response["documents"]

        if count == total_num:
            break
        else:
            start = count - 1


def update_metadata(
    token: str,
    lib: str,
    name: t.Optional[str] = None,
    description: t.Optional[str] = None,
    public: t.Optional[bool] = False,
):

    params = {}
    if name is not None:
        params["name"] = name
    if description is not None:
        params["description"] = description
    if public is not None:
        params["public"] = bool(public)

    url = urls.make_url(urls.urls["libraries"]["change"], lib)

    data = http.put(token, url, params)

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
            raise e.AdsApiError(f"Unknown error code {data.status}")


def transfer(token: str, lib: str, email: str):
    url = urls.make_url(urls.urls["libraries"]["transfer"], lib)

    data = http.post(token, url, {"email": email})

    if data.status != 200:
        if data.status == 400:
            raise e.MalformedRequest
        elif data.status == 403:
            raise e.InsufficentPermisions
        elif data.status == 404:
            raise e.NoADSAccount
        else:
            raise e.AdsApiError(f"Unknown error code {data.status}")


def new(
    token: str,
    name: t.Optional[str] = None,
    description: t.Optional[str] = None,
    public: t.Optional[bool] = None,
    bibcode: t.Optional[t.Union[str, t.List[str]]] = None,
):

    params: t.Dict[t.Any, t.Any] = {}
    if name is not None:
        params["name"] = name
    if description is not None:
        params["description"] = description
    if public is not None:
        params["public"] = False
        if public:
            params["public"] = True
    if bibcode is not None:
        params["bibcode"] = utils.ensure_list(bibcode)

    url = urls.make_url(urls.urls["libraries"]["view"])

    data = http.post(token, url, data=params, json=True)

    if data.status != 200:
        if data.status == 400:
            raise e.MalformedRequest
        elif data.status == 409:
            raise e.LibraryAllreadyExists
        else:
            raise e.AdsApiError(f"Unknown error code {data.status}")

    return data.response


def delete(token: str, lib: str):
    url = urls.make_url(urls.urls["libraries"]["change"], lib)

    data = http.delete(token, url)

    if data.status != 200:
        if data.status == 400:
            raise e.MalformedRequest
        elif data.status == 403:
            raise e.InsufficentPermisions
        elif data.status == 410:
            raise e.LibraryDoesNotExist
        else:
            raise e.AdsApiError(f"Unknown error code {data.status}")


def add(token: str, lib: str, bibcode: str):
    url = urls.make_url(urls.urls["libraries"]["change"], lib)

    bibs = utils.ensure_list(bibcode)

    data = http.post(token, url, {"action": "add", "bibcode": bibs})

    if data.status != 200:
        if data.status == 400:
            raise e.MalformedRequest
        elif data.status == 403:
            raise e.InsufficentPermisions
        else:
            raise e.AdsApiError(f"Unknown error code {data.status}")

    if len(bibs) != data.response["number_added"]:
        raise e.AdsApiError(
            f"Bad number of bibcodes added tried {len(bibs)} got {data.response['number_added']}"
        )


def remove(token: str, lib: str, bibcode: str):
    url = urls.make_url(urls.urls["libraries"]["change"], lib)

    bibs = utils.ensure_list(bibcode)
    data = http.post(token, url, {"action": "remove", "bibcode": bibs})

    if data.status != 200:
        if data.status == 400:
            raise e.MalformedRequest
        elif data.status == 403:
            raise e.InsufficentPermisions
        else:
            raise e.AdsApiError(f"Unknown error code {data.status}")

    if len(bibs) != data.response["number_removed"]:
        raise e.AdsApiError(
            f"Bad number of bibcodes removed tried {len(bibs)} got {data.response['number_removed']}"
        )
