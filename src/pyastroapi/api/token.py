# SPDX-License-Identifier: BSD-3-Clause

import os
import typing as t


def get_token(filename: str = "~/.ads/dev_key") -> t.Union[str, None]:
    if "ADS_DEV_KEY" in os.environ:
        return os.environ["ADS_DEV_KEY"]

    filename = os.path.expanduser(filename)
    if os.path.exists(filename):
        with open(filename, "r") as f:
            return f.readline().strip()
    return None


def save_token(token: str, filename: str = "~/.ads/dev_key") -> None:
    filename = os.path.expanduser(filename)
    if os.path.exists(filename):
        with open(filename, "w") as f:
            print(token, file=f)
    return
