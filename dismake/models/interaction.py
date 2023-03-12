from __future__ import annotations
from typing import Any, Optional

from pydantic import BaseModel
from ..types import SnowFlake
from .user import Member, User


__all__ = (
    "Interaction",
    "CommandData",
    "ComponentData"
)

class ResolvedData(BaseModel):
    users: Optional[Any]
    members: Optional[Any]
    channels: Optional[Any]
    roles: Optional[Any]
    messages: Optional[Any]
    attachments: Optional[Any]


class CommandData(BaseModel):
    id: SnowFlake
    name: str
    type: int
    resolved: Optional[ResolvedData]
    options: Optional[list[CommandData]]
    guild_id: Optional[int]
    target_id: Optional[int]


class ComponentData(BaseModel):
    custom_id: SnowFlake
    component_type: int
    values: Optional[list[Any]]


class Interaction(BaseModel):
    id: SnowFlake
    application_id: SnowFlake
    type: int
    data: Optional[Any]
    guild_id: SnowFlake
    channel_id: SnowFlake
    member: Optional[Member]
    user: User
    token: str
    version: int
    message: Any
    app_permissions: Optional[str]
    locale: Any
    guild_locale: Any
