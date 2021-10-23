# SPDX-License-Identifier: BSD-3-Clause

import typing as t


def ensure_list(s: t.Union[str, t.List[str]]) -> t.List[str]:
    return s if isinstance(s, list) else [s]
