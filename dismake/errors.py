from __future__ import annotations
from typing import TYPE_CHECKING, Union

if TYPE_CHECKING:
    from .commands import SlashCommand
    from .models import Interaction
    from .app_commands import AppCommand, Group

__all__ = (
    "DismakeException",
    "NotImplemented",
    "CommandInvokeError",
    "InteractionResponded",
    "InteractionNotResponded",
    "ComponentException",
)


class DismakeException(Exception):
    """Base dismake exception."""


class NotImplemented(DismakeException):
    """Raise when a unknown command invoke."""


class CommandInvokeError(DismakeException):
    """TODO"""

    def __init__(self, command: Union[Group, AppCommand], exception: Exception) -> None:
        self.command = command
        self.exception = exception
        super().__init__(f"Command {command.name!r} raised an exception: {exception}")


class InteractionResponded(DismakeException):
    def __init__(self, interaction: Interaction) -> None:
        self.interaction = interaction
        super().__init__(f"{interaction.id!r} Interaction already responded.")


class InteractionNotResponded(DismakeException):
    def __init__(self, interaction: Interaction) -> None:
        self.interaction = interaction
        super().__init__(f"{interaction.id!r} The interaction is not responded.")


class ComponentException(DismakeException):
    """Base Exception for house."""
