# SPDX-License-Identifier: BSD-3-Clause

import typing as t

__all__ = ["ensure_list", "ensure_str"]


def ensure_list(s: t.Union[str, t.List[str]]) -> t.List[str]:
    """Given a string or list of strings return a list of strings

    Args:
        s (t.Union[str, t.List[str]]): a string or list of strings

    Returns:
        t.List[str]:  List of strings
    """
    return s if isinstance(s, list) else [s]


def ensure_str(s: t.Union[str, t.List[str]]) -> str:
    """Given a string or list of strings return a  comma separated string of all elements

    Args:
        s (t.Union[str, t.List[str]]): a string or list of strings

    Returns:
        str: CSV string
    """
    return s if isinstance(s, str) else ",".join(s)
