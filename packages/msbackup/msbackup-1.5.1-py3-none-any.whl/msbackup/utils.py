# -*- coding: utf-8 -*-
"""Служебные функции."""


def dequote(s):
    """
    If a string has single or double quotes around it, remove them.

    Make sure the pair of quotes match.
    If a matching pair of quotes is not found, return the string unchanged.
    """
    if (s is not None and len(s) > 1 and
            (s[0] == s[-1]) and s.startswith(("'", '"'))):
        return s[1:-1]
    return s


class EmptyListString(object):
    """Empty list string."""

    def __len__(self):
        """Length of string."""
        return 0

    def split(self, *args):
        """Split string to token list."""
        return []
