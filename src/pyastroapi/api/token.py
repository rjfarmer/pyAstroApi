# SPDX-License-Identifier: BSD-3-Clause

import os
import typing as t

__all__ = ["get_token", "save_token", "get_orcid", "save_orcid"]


def get_token(filename: str = "~/.ads/dev_key") -> t.Union[str, None]:
    """Get a user's ADS token

    First looks for the environment variable ADS_DEV_KEY then looks in filename

    Args:
        filename (str, optional):Filename to read token from. Defaults to "~/.ads/dev_key".

    Returns:
        t.Union[str, None]: ADS token
    """
    if "ADS_DEV_KEY" in os.environ:
        return os.environ["ADS_DEV_KEY"]

    filename = os.path.expanduser(filename)
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return f.readline().strip()
    return None


def save_token(token: str, filename: str = "~/.ads/dev_key") -> None:
    """Save a users ADS token

    Args:
        filename (str, optional): Filename to save token to. Defaults to "~/.ads/dev_key".

    """
    filename = os.path.expanduser(filename)
    with open(filename, "w") as f:
        print(token, file=f)
    return


def get_orcid(filename: str = "~/.ads/orcid") -> t.Union[str, None]:
    """Get a user's ORCID

    Args:
        filename (str, optional):Filename to read token from. Defaults to "~/.ads/orcid".

    Returns:
        t.Union[str, None]: ORCID
    """
    filename = os.path.expanduser(filename)
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return f.readline().strip()
    return None


def save_orcid(token: str, filename: str = "~/.ads/orcid") -> None:
    """Save a user's ORCID

    Args:
        filename (str, optional): Filename to save the ORCID to. Defaults to "~/.ads/orcid".

    """
    filename = os.path.expanduser(filename)
    with open(filename, "w") as f:
        print(token, file=f)
    return
