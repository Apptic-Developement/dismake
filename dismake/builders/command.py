from __future__ import annotations

from typing import Any, Dict, List, Optional, Union
from ..interaction import Interaction
from ..types import SnowFlake
from ..enums import CommandType, OptionType


__all__ = ("SlashCommandBuilder", "Option", "Choice")


class Choice:
    def __init__(self, name: str, value: Optional[Union[str, int, float, bool]] = None):
        self.name = name
        self.value = value or name


class SlashCommandBuilder:
    def __init__(
        self,
        name: str,
        description: str = "No description provided",
        *,
        name_localizations: Optional[Dict[str, str]] = None,
        description_localizations: Optional[Dict[str, str]] = None,
        nsfw: Optional[bool] = False,
        guild_id: Optional[SnowFlake] = None,
        options: Optional[List[Option]] = None,
        default_member_permissions: Optional[str] = None,
        dm_permission: Optional[bool] = True,
    ):
        self.name = name
        self.description = description
        self.name_localizations = name_localizations
        self.description_localizations = description_localizations
        self.nsfw = nsfw
        self.guild_id = guild_id
        self.options = options
        self.default_member_permissions = default_member_permissions
        self.dm_permission = dm_permission
        self.type: int = CommandType.SLASH

    async def callback(self, interaction: Interaction) -> Any:
        ...


class Option:
    def __init__(
        self,
        name: str,
        description: Optional[str] = "No description provided",
        *,
        type: int = OptionType.STRING,
        name_localizations: Optional[dict[str, str]] = None,
        description_localizations: Optional[dict[str, str]] = None,
        required: Optional[bool] = False,
        choices: Optional[List[Choice]] = None,
        options: Optional[List[Option]] = None,
        channel_types: Optional[List[str]] = None,
        min_value: Optional[int] = None,
        max_value: Optional[int] = None,
        autocomplete: Optional[bool] = None,
    ):
        self.name = name
        self.description = description
        self.type = type
        self.name_localizations = name_localizations
        self.description_localizations = description_localizations
        self.required = required
        self.choices = choices
        self.options = options
        self.channel_types = channel_types
        if type == OptionType.STRING:
            self.min_value = None
            self.max_value = None
            self.min_length = max_value
            self.max_length = max_value
        elif type == OptionType.INTEGER:
            self.min_value = max_value
            self.max_value = max_value
            self.min_length = None
            self.max_length = None
        else:
            self.min_value = None
            self.max_value = None
            self.min_length = None
            self.max_length = None
        self.autocomplete = autocomplete
