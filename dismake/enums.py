from __future__ import annotations

from enum import Enum

__all__ = (
    "DefaultAvatar",
    "InteractionType",
    "InteractionResponseType",
    "InteractionResponseFlags",
    "CommandType",
    "OptionType"
)

class DefaultAvatar(Enum):
    blurple = 0
    grey = 1
    gray = 1
    green = 2
    orange = 3
    red = 4

    def __str__(self) -> str:
        return self.name


class InteractionType(Enum):
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    MODAL_SUBMIT = 5

class InteractionResponseType(Enum):
    PONG = 1
    CHANNEL_MESSAGE_WITH_SOURCE = 4
    DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE = 5
    DEFERRED_UPDATE_MESSAGE = 6
    UPDATE_MESSAGE =  7
    APPLICATION_COMMAND_AUTOCOMPLETE_RESULT = 8
    MODAL = 9

class InteractionResponseFlags(Enum):
    EPHEMERAL = 1 << 6

class CommandType(Enum):
    SLASH = 1
    USER = 2
    MESSAGE = 3


class OptionType(Enum):
    SUB_COMMAND = 1
    SUB_COMMAND_GROUP = 2
    STRING = 3
    INTEGER = 4
    BOOLEAN = 5
    USER = 6
    CHANNEL = 7
    ROLE = 8
    MENTIONABLE = 9
    NUMBER = 10