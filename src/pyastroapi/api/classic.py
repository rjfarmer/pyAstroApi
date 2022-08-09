# SPDX-License-Identifier: BSD-3-Clause

from . import exceptions as e
from . import urls
from . import http

__all__ = ["mirrors", "user", "signin"]


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

    if r.status != 200:
        raise e.AdsApiError(r.response["error"])

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
        raise e.AdsApiError(r.response["error"])

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
        raise e.AdsApiError(r.response["error"])

    return r.response
