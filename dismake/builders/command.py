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

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name, "value": self.value}


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

    async def callback(self, interaction: Interaction) -> Any:
        ...

    async def autocomplete(self, interaction: Interaction) -> Any:
        ...

    def to_dict(self) -> Dict[str, Any]:
        base = {
            "type": CommandType.SLASH,
            "name": self.name,
            "description": self.description,
        }
        if self.name_localizations is not None:
            base["name_localization"] = self.name_localizations
        if self.description_localizations is not None:
            base["description_localization"] = self.description_localizations
        if self.nsfw is not None:
            base["nsfw"] = self.nsfw
        if self.guild_id is not None:
            base["guild_id"] = self.guild_id
        if self.options is not None:
            base["options"] = [option.to_dict() for option in self.options]
        if self.default_member_permissions is not None:
            base["default_member_permission"] = self.default_member_permissions
        if self.dm_permission is not None:
            base["dm_permission"] = self.dm_permission
        return base


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
            self.min_length = min_value
            self.max_length = max_value
        elif type == OptionType.INTEGER:
            self.min_value = min_value
            self.max_value = max_value
            self.min_length = None
            self.max_length = None
        else:
            self.min_value = None
            self.max_value = None
            self.min_length = None
            self.max_length = None
        self.autocomplete = autocomplete

    def to_dict(self) -> Dict[str, Any]:
        base = {"type": self.type, "name": self.name, "description": self.description}

        if self.name_localizations is not None:
            base["name_localization"] = self.name_localizations
        if self.description_localizations is not None:
            base["description_localization"] = self.description_localizations
        if self.required is not None:
            base["required"] = self.required
        if self.choices is not None:
            base["choices"] = [choice.to_dict() for choice in self.choices]
        if self.options is not None:
            base["options"] = [option.to_dict() for option in self.options]
        if self.channel_types is not None:
            base["channel_types"] = self.channel_types
        if self.min_length is not None:
            base["min_length"] = self.min_length
        if self.max_length is not None:
            base["max_length"] = self.max_length
        if self.min_value is not None:
            base["min_value"] = self.min_value
        if self.max_value is not None:
            base["max_value"] = self.max_value
        if self.autocomplete is not None:
            base["autocomplete"] = self.autocomplete

        return base
