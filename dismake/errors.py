from __future__ import annotations
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .commands import SlashCommand

class DismakeException(Exception):
    """Base dismake exception."""

class NotImplemented(DismakeException):
    """Raise when a unknown command invoke."""

class CommandInvokeError(DismakeException):
    """TODO"""
    def __init__(self, command: SlashCommand, exception: Exception) -> None:
        self.command = command
        self.exception = exception
        super().__init__(f"Command {command.name!r} raised an exception: {exception}")
