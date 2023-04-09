from __future__ import annotations


class DismakeException(Exception):
    """Base dismake exception."""

class NotImplemented(DismakeException):
    """Raise when a unknown command invoke."""

