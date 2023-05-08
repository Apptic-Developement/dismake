from __future__ import annotations

from datetime import datetime
from typing import Optional, Union
from pydantic import BaseModel, PrivateAttr
from fastapi import Request
from ..types import SnowFlake
from ..enums import ChannelType
from .permission_overwrites import PermissionOverwrites


__all__ = ("PartialMessagable", "TextChannel", "CategoryChannel", "Channel")



class PartialMessagable(BaseModel):
    _request: Request = PrivateAttr()
    id: SnowFlake
    type: int

    @property
    def mention(self) -> str:
        return f"<#{self.id}>"

    def __repr__(self) -> str:
        return f"<Channel id={self.id}>"

    class Config: arbitrary_types_allowed = True


class TextChannel(PartialMessagable):
    guild_id: Optional[int]
    position: Optional[int]
    permission_overwrites: list[PermissionOverwrites] = list()
    name: Optional[str]
    topic: Optional[str]
    nsfw: Optional[bool] = False
    last_message_id: Optional[int]
    parent_id: Optional[int]
    last_pin_timestamp: Optional[datetime]
    permissions: Optional[str]
    rate_limit_per_user: Optional[int]
    default_auto_archive_duration: Optional[int]
    created_at: Optional[datetime]

    def __repr__(self) -> str:
        return f"<TextChannel name={self.name}>"
    
    def __str__(self) -> str:
        return f"{self.name}"


class CategoryChannel(PartialMessagable):
    permission_overwrites: list[PermissionOverwrites] = list()
    name: str
    nsfw: Optional[bool] = False
    position: int
    guild_id: SnowFlake

    def __repr__(self) -> str:
        return f"<CategoryChannel name={self.name}>"
    
    def __str__(self) -> str:
        return self.name
Channel = Union[TextChannel, CategoryChannel]