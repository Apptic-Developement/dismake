from __future__ import annotations
from typing import Optional
from dismake.enums import CommandType, OptionType

from dismake.types.snowflake import SnowFlake

from .command import validate_name


__all__ = (
    "Group",
    "GroupCommand"
)


class Group:
    def __init__(
        self,
        name: str,
        description: str,
        parent: Optional[Group] = None,
        guild_id: Optional[SnowFlake] = None
    ) -> None:
        self._name = validate_name(name)
        self._description = description
        self._parent = parent
        self._guild_id = guild_id
        self._commands: list[GroupCommand]
        if parent:
            self._type = OptionType.SUB_COMMAND_GROUP
        else:
            self._type = CommandType.SLASH

    

class GroupCommand:
    def __init__(self) -> None:
        pass