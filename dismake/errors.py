from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from .commands import Command
    from .models import Interaction


__all__ = (
    "DismakeException",
    "NotImplemented",
    "CommandInvokeError",
    "InteractionResponded",
    "InteractionNotResponded",
    "ComponentException",
    "PluginException",
    "CommandException",
)


class DismakeException(Exception):
    """Base dismake exception."""


class PluginException(Exception):
    """Base dismake exception."""


class NotImplemented(DismakeException):
    """Raise when a unknown command invoke."""


class CommandInvokeError(DismakeException):
    """When a command fails to invoke."""

    def __init__(self, command: Command, exception: Exception) -> None:
        self.command = command
        self.exception = exception
        super().__init__(f"Command {command.name!r} raised an exception: {exception}")


class CommandException(DismakeException):
    """Raise when a command raised an exception."""


class InteractionResponded(DismakeException):
    def __init__(self, interaction: Interaction) -> None:
        self.interaction = interaction
        super().__init__(f"{interaction.id!r} Interaction already responded.")


class InteractionNotResponded(DismakeException):
    def __init__(self, interaction: Interaction) -> None:
        self.interaction = interaction
        super().__init__(f"{interaction.id!r} The interaction is not responded.")


class ComponentException(DismakeException):
    """Base Exception for View."""
