from __future__ import annotations
from typing import Any, Optional

from pydantic import BaseModel
from ..types import SnowFlake
from .user import Member, User
from ..enums import InteractionType


__all__ = ("Interaction", "CommandData", "ComponentData")


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
    type: int
    token: str
    member: Optional[Member]
    id: SnowFlake
    guild_id: SnowFlake
    app_permissions: str
    guild_locale: Optional[str]
    locale: Optional[str]
    data: CommandData
    channel_id: SnowFlake


# make = {
#     "type": 2,
#     "token": "A_UNIQUE_TOKEN",
#     "member": {
#         "user": {
#             "id": "53908232506183680",
#             "username": "Mason",
#             "avatar": "a_d5efa99b3eeaa7dd43acca82f5692432",
#             "discriminator": "1337",
#             "public_flags": 131141,
#         },
#         "roles": ["539082325061836999"],
#         "premium_since": None,
#         "permissions": "2147483647",
#         "pending": False,
#         "nick": None,
#         "mute": False,
#         "joined_at": "2017-03-13T19:19:14.040000+00:00",
#         "is_pending": False,
#         "deaf": False,
#     },
#     "id": "786008729715212338",
#     "guild_id": "290926798626357999",
#     "app_permissions": "442368",
#     "guild_locale": "en-US",
#     "locale": "en-US",
#     "data": {
#         "options": [{"type": 3, "name": "cardname", "value": "The Gitrog Monster"}],
#         "type": 1,
#         "name": "cardsearch",
#         "id": "771825006014889984",
#     },
#     "channel_id": "645027906669510667",
# }
