from __future__ import annotations
from collections.abc import Callable
from typing import TypedDict

__all__ = (
    "CommandTypes",
    "OptionTypes",
    "SubCommandDict"
)
class CommandTypes:
    SLASH = 1
    USER = 2
    MESSAGE = 3


class OptionTypes:
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
    
    
class SubCommandDict(TypedDict):
    name: str
    description: str
    callback: Callable

