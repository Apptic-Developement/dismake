from __future__ import annotations
from typing import Any, Optional
from fastapi import Request

from pydantic import BaseModel

from dismake.enums import InteractionResponseType
from .types import SnowFlake
from .models import Member
from .api import API


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
    request: Request
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

    _responded = False

    async def respond(
        self, content: str, *, tts: bool = False, ephemeral: bool = False
    ):
        return await self.request.app._http.client.request(
            method="POST",
            url=f"/interactions/{self.id}/{self.token}/callback",
            json={
                "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE.value,
                "data": {"content": content, "tts": tts},
            },
            headers=self.request.app._http.headers,
        )

    async def defer(self, thinking: bool = True):
        return await self.request.app._http.client.request(
            method="POST",
            url=f"/interactions/{self.id}/{self.token}/callback",
            json={
                "type": InteractionResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE.value,
                "data": {},
            },
            headers=self.request.app._http.headers,
        )

    class Config:
        arbitrary_types_allowed = True


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
