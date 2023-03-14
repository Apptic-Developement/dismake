from __future__ import annotations
from typing import Optional
from pydantic import validator

from ..types import SnowFlake
from .option import Option
from ..enums import CommandType
from .base import BaseSlashCommand

__all__ = ("SlashCommand",)


class SlashCommand(BaseSlashCommand):
    type: int = CommandType.SLASH
    name: str
    description: str
    guild_id: Optional[SnowFlake] = None
    name_localizations: Optional[dict[str, str]] = None
    description_localizations: Optional[dict[str, str]] = None
    options: Optional[list[Option]] = None
    default_member_permissions: Optional[str] = None
    dm_permission: Optional[bool] = True
    nsfw: Optional[bool] = False

    def callback(self, interaction):
        print(interaction)

    @validator("type")
    def validate_type(cls, value: int):
        if value != CommandType.SLASH:
            raise TypeError("You can not override slash command type.")
        return value
    
