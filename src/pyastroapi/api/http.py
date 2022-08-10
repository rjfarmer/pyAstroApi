# SPDX-License-Identifier: BSD-3-Clause

import requests
import os
import typing as t

from dataclasses import dataclass

from . import utils

__all__ = [
    "get",
    "post",
    "put",
    "delete",
    "post_bibcodes",
    "bigquery_bibcodes",
    "download_file",
]


class _BearerAuth(requests.auth.AuthBase):
    """Handles setting the ADS token in http requests"""

    def __init__(self, token: str) -> None:
        self.token = token

    def __call__(self, r):
        r.headers["authorization"] = "Bearer " + str(self.token)
        return r


class FileDownloadFailed(Exception):
    pass


HttpResponseResponse_t = t.Any

Payload_t = t.Union[
    t.Dict[str, t.List[str]],
    t.Dict[str, str],
    t.Dict[str, t.Sequence[str]],
    t.Dict[str, bool],
    t.Dict[str, _BearerAuth],
    None,
]


@dataclass
class ADSLimits:
    """Stores the last set of ADS limits received"""

    limit: int = -1
    remaining: int = -1
    reset: int = -1

    def __init__(self, header):
        try:
            self.limit = header["X-RateLimit-Limit"]
            self.remaining = header["X-RateLimit-Remaining"]
            self.reset = header["X-RateLimit-Reset"]
        except KeyError:
            pass


@dataclass
class HttpResponse:
    response: HttpResponseResponse_t
    status: int
    limits: ADSLimits


def get(
    token: str, url: str, data: Payload_t = None, json: bool = True
) -> HttpResponse:
    """Perform a HTTP Get request

    Args:
        token (str): ADS Token
        url (str): URL to get. This should usually include some sort of extra identifier
        data (Payload_t, optional): Any additional data being passed, thats not in the URL. Defaults to None.
        json (bool, optional): Whether to return the data in a JSON compatible format. Defaults to True.

    Returns:
        HttpResponse:
    """
    if data is None:
        data = {}  # type:ignore

    r = requests.get(
        url,
        auth=_BearerAuth(token),
        params=data,
    )

    response_code = r.status_code

    if json:
        return HttpResponse(r.json(), response_code, ADSLimits(r.headers))
    else:
        return HttpResponse(r.text, response_code, ADSLimits(r.headers))


def post(
    token: str,
    url: str,
    data: Payload_t = None,
    params: t.Any = None,
    json: bool = True,
) -> HttpResponse:
    """Perform a HTTP Post request

    Args:
        token (str): ADS Token
        url (str): URL to post to
        data (Payload_t, optional): Data being sent. Defaults to None.
        params (Payload_t, optional): Data being sent via the url and not the post dict. Defaults to None.
        json (bool, optional): Whether to return the data in a JSON compatible format. Defaults to True.

    Returns:
        HttpResponse:
    """

    args = {}  # type:ignore
    args["auth"] = _BearerAuth(token)

    if data is not None:
        args["json"] = data
        args["headers"] = {
            "Content-Type": "application/json",
            "Accept": "application/json",
        }

    if params is not None:
        args["params"] = params

    r = requests.post(url, **args)  # type:ignore

    response_code = r.status_code

    if json:
        return HttpResponse(r.json(), response_code, ADSLimits(r.headers))
    else:
        return HttpResponse(r.text, response_code, ADSLimits(r.headers))


def put(token: str, url: str, data: Payload_t) -> HttpResponse:
    """Perform a HTTP Put request

    Args:
        token (str): ADS Token
        url (str): URL to post to
        data (Payload_t, optional): Data being sent. Defaults to None.

    Returns:
        HttpResponse:
    """

    r = requests.put(
        url,
        auth=_BearerAuth(token),
        headers={"Content-Type": "application/json"},
        json=data,
    )

    response_code = r.status_code

    return HttpResponse(r.json(), response_code, ADSLimits(r.headers))


def delete(token: str, url: str) -> HttpResponse:
    """Perform a HTTP Delete request

    Args:
        token (str): ADS Token
        url (str): URL to post to

    Returns:
        HttpResponse:
    """
    r = requests.delete(
        url,
        auth=_BearerAuth(token),
    )

    response_code = r.status_code

    return HttpResponse("", response_code, ADSLimits(r.headers))


def post_bibcodes(
    token: str, url: str, bibcodes: t.Union[str, t.List[str]], multi_bibs: bool = True
) -> HttpResponse:
    """Perform a HTTP Post request with a list of bibcodes

    Args:
        token (str): ADS Token
        url (str): URL to post to
        bibcodes (t.Union[str, t.List[str]]): Either a single bibcode or a list of bibcodes
        multi_bibs (bool): Some end points care whether you use bibcode or bibcodes and thats not consistent with the actual number of bibcodes used
    Returns:
        HttpResponse:
    """

    if isinstance(bibcodes, list):
        if multi_bibs:
            data = {"bibcodes": bibcodes}
        else:
            # Some end points want bibcode even with plural bibcodes
            data = {"bibcode": bibcodes}
    else:
        data = {"bibcode": utils.ensure_list(bibcodes)}

    return post(token, url, data)


def bigquery_bibcodes(
    token: str,
    url: str,
    bibcodes: t.Union[str, t.List[str]],
    params: t.Any,
) -> HttpResponse:
    """Perform a ADS Big query with a list of bibcodes

    Args:
        token (str): ADS Token
        url (str): URL to post to
        bibcodes (t.Union[str, t.List[str]]): Either a single bibcode or a list of bibcodes
        params (dict) : Extra params sent
    Returns:
        HttpResponse:
    """

    data = "bibcode\n" + "\n".join(utils.ensure_list(bibcodes))

    r = requests.post(
        url,
        params=params,
        auth=_BearerAuth(token),
        data=data,
    )

    response_code = r.status_code

    return HttpResponse(r.json(), response_code, ADSLimits(r.headers))


def download_file(url: str, filename: str):
    """Download a file to filename

    On return you should check if the file exists to see if it succeeded.

    Args:
        url (str): URL to download from
        filename (str): Filename to save file to.

    Raises:
        FileDownloadFailed: _description_
    """

    headers = {
        "User-Agent": "Mozilla/5.0 (X11; Fedora; Linux x86_64; rv:96.0) Gecko/20100101 Firefox/96.0",
        "DNT": "1",
        "Accept": "*/*",
        "Host": "www.google.com",
        "Connection": "keep-alive",
    }

    r = requests.get(url, stream=True, headers=headers, allow_redirects=True)
    with open(filename, "wb") as fd:
        for chunk in r.iter_content(chunk_size=1024):
            fd.write(chunk)

    # Check if a pdf file was downloaded
    with open(filename, "rb") as fd:
        line = fd.readline()

    if line.startswith(b"<!DOCTYPE html"):
        os.remove(filename)
        # html = os.path.abspath(filename.replace('.pdf','.html'))
        # shutil.move(filename,html)
        # webbrowser.open(f'file://{html}')
        raise FileDownloadFailed("Annoying site gave us a html file and not a pdf")
