# SPDX-License-Identifier: BSD-3-Clause

import typing as t

from . import exceptions as e
from . import urls
from . import http
from . import utils

__all__ = [
    "list_all",
    "get_permissions",
    "get",
    "update_metadata",
    "transfer",
    "new",
    "delete",
    "add",
    "remove",
    "edit",
]


def list_all(token: str):
    """List all libraries the user has

    Args:
        token (str): ADSABS token

    Raises:
        e.AdsApiError: _description_

    Returns:
        _type_: _description_
    """

    url = urls.make_url(urls.urls["libraries"]["view"])

    r = http.get(token, url)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response


def get_permissions(token: str, lib: str):

    url = urls.make_url(urls.urls["libraries"]["permission"], lib)

    r = http.get(token, url)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response


def get(token: str, lib: str):
    start = 0
    count = 0
    while True:
        url = urls.make_url(urls.urls["libraries"]["view"], lib, "?start=" + str(start))

        r = http.get(token, url)

        if r.status != 200:
            raise e.AdsApiError(r.response["error"])

        total_num = int(r.response["metadata"]["num_documents"])

        if len(r.response["documents"]) == 0:
            # Total_num lies sometimes so track when we stop getting new papers
            break

        count += len(r.response["documents"])

        yield from r.response["documents"]

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

    r = http.put(token, url, params)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])


def transfer(token: str, lib: str, email: str):
    url = urls.make_url(urls.urls["libraries"]["transfer"], lib)

    r = http.post(token, url, {"email": email})

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])


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

    r = http.post(token, url, data=params, json=True)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    return r.response


def delete(token: str, lib: str):
    url = urls.make_url(urls.urls["libraries"]["change"], lib)

    r = http.delete(token, url)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])


def add(token: str, lib: str, bibcode: str):
    url = urls.make_url(urls.urls["libraries"]["change"], lib)

    bibs = utils.ensure_list(bibcode)

    r = http.post(token, url, {"action": "add", "bibcode": bibs})

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    if len(bibs) != r.response["number_added"]:
        raise e.AdsApiError(
            f"Bad number of bibcodes added tried {len(bibs)} got {r.response['number_added']}"
        )


def remove(token: str, lib: str, bibcode: str):
    url = urls.make_url(urls.urls["libraries"]["change"], lib)

    bibs = utils.ensure_list(bibcode)
    r = http.post(token, url, {"action": "remove", "bibcode": bibs})

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

    if len(bibs) != r.response["number_removed"]:
        raise e.AdsApiError(
            f"Bad number of bibcodes removed tried {len(bibs)} got {r.response['number_removed']}"
        )


def edit(
    token: str,
    lib: str,
    email: str,
    read: bool = False,
    write: bool = False,
    admin: bool = False,
):
    url = urls.make_url(urls.urls["libraries"]["permission"], lib)

    data = {
        "email": email,
        "permission": {
            "read": read,
            "write": write,
            "admin": admin,
        },
    }

    r = http.post(token, url, data)

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])
