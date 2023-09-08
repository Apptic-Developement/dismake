from __future__ import annotations

from typing import TYPE_CHECKING, Sequence

if TYPE_CHECKING:
    ...

__all__: Sequence[str] = (
    "DismakeException",
    "CommandInvokeException",
    "PluginException",
    "ViewException",
    "HttpException",
)


class DismakeException(Exception):
    ...


class CommandInvokeException(DismakeException):
    ...


class PluginException(DismakeException):
    ...


class ViewException(DismakeException):
    ...


class HttpException(DismakeException):
    ...
