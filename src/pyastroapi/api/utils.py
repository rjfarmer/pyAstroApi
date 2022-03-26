# SPDX-License-Identifier: BSD-3-Clause

import typing as t


def ensure_list(s: t.Union[str, t.List[str]]) -> t.List[str]:
    return s if isinstance(s, list) else [s]


def ensure_str(s: t.Union[str, t.List[str]]) -> str:
    return s if isinstance(s, str) else ",".join(s)
