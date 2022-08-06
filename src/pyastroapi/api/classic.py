# SPDX-License-Identifier: BSD-3-Clause

from . import exceptions as e
from . import urls
from . import http
from . import utils
import typing as t


def mirrors(token: str):
    """Get a list of ADS classic mirror

    https://ui.adsabs.harvard.edu/help/api/api-docs.html#get-/harbour/mirrors

    Args:
        token (str): ADSABS token

    Returns:
        list[str]: List of available mirrors
    """

    url = urls.make_url(urls.urls["classic"]["mirrors"])

    r = http.get(token, url, {}, True)

    return r.response


def user(token: str):
    """Get ADS classic registration email and mirror

    https://ui.adsabs.harvard.edu/help/api/api-docs.html#get-/harbour/user

    Args:
        token (str): ADSABS token

    Returns:
        Dict with:
            str: Email
            str: Classic mirror
            str: twopointoh_email
    """

    url = urls.make_url(urls.urls["classic"]["user"])

    r = http.get(token, url, {}, True)

    if r.status != 200:
        if r.status == 400:
            raise e.ClassicUserDidNotMakeAccount
        else:
            raise e.AdsApiError(f"Unknown error code {r.status}")

    return r.response


def signin(token: str, email: str, password: str, mirror: str):
    """Sign into ADS Classic account and link it to your main ADS account

    https://ui.adsabs.harvard.edu/help/api/api-docs.html#post-/harbour/auth/classic

    Args:
        token (str): ADSABS token
        email (str): Classic email
        password (str): Classic password
        mirror (str): Classic mirror

    Returns:
        str: Email
        str: Classic mirror
        str: twopointoh_email
    """

    url = urls.make_url(urls.urls["classic"][""])

    data = {
        "classic_email": email,
        "classic_mirror": password,
        "classic_password": mirror,
    }

    r = http.post(token, url, data, True)

    if r.status != 200:
        if r.status == 400:
            raise e.MalformedRequest
        elif r.status == 404:
            raise e.AuthenticationFailed
        elif r.status == 500:
            raise e.ClassicNoCookie
        elif r.status == 504:
            raise e.ClassicTimeOut
        else:
            raise e.AdsApiError(f"Unknown error code {r.status}")

    return r.response