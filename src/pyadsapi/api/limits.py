# SPDX-License-Identifier: BSD-3-Clause

import typing as t

limit = 5000
remaining = 5000
reset = -1


def update_limits(header: t.MutableMapping[str,str]) -> None:
    try:
        limit = header['X-RateLimit-Limit']
        remaining = header['X-RateLimit-Remaining']
        reset = header['X-RateLimit-Reset']
    except KeyError:
        pass

    print(limit, remaining, reset)
    return