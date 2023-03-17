from __future__ import annotations
from typing import Any, Optional, Union

from dismake.models.user import User

from fastapi import Request
from pydantic import BaseModel
from .params import handle_send_params
from .enums import InteractionResponseType
from .types import SnowFlake
from .models import Member
from .enums import MessageFlags


__all__ = ("Interaction", "CommandData", "ComponentData", "ResolvedData")


class ResolvedData(BaseModel):
    users: Optional[Any]
    members: Optional[Any]
    channels: Optional[Any]
    roles: Optional[Any]
    messages: Optional[Any]
    attachments: Optional[Any]


class CommandDataOption(BaseModel):
    name: str
    type: int
    value: Optional[Union[str, int, float]]
    options: Optional[list[CommandDataOption]]
    focused: Optional[bool]


class CommandData(BaseModel):
    id: SnowFlake
    name: str
    type: int
    resolved: Optional[ResolvedData]
    options: Optional[list[CommandDataOption]]
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
    user: Optional[User]
    id: SnowFlake
    application_id: SnowFlake
    guild_id: SnowFlake
    app_permissions: str
    guild_locale: Optional[str]
    locale: Optional[str]
    data: Union[CommandData, ComponentData, CommandDataOption]
    channel_id: SnowFlake

    async def respond(
        self, content: str, *, tts: bool = False, ephemeral: bool = False
    ):
        return await self.request.app._http.client.request(
            method="POST",
            url=f"/interactions/{self.id}/{self.token}/callback",
            json={
                "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE.value,
                "data": handle_send_params(
                    content=content, tts=tts, ephemeral=ephemeral
                ),
            },
            headers=self.request.app._http.headers,
        )

    async def defer(self, thinking: bool = True):
        return await self.request.app._http.client.request(
            method="POST",
            url=f"/interactions/{self.id}/{self.token}/callback",
            json={
                "type": InteractionResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE.value,
                "data": {"flags": MessageFlags.LOADING.value} if not thinking else None,
            },
            headers=self.request.app._http.headers,
        )

    async def send_followup(
        self, content: str, *, tts: bool = False, ephemeral: bool = False
    ):
        return await self.request.app._http.client.request(
            method="POST",
            url=f"/webhooks/{self.application_id}/{self.token}",
            json=handle_send_params(content=content, tts=tts, ephemeral=ephemeral),
            headers=self.request.app._http.headers,
        )

    class Config:
        arbitrary_types_allowed = True


normal = {
    "app_permissions": "4398046511103",
    "application_id": "1071851326234951770",
    "channel_id": "1070755073866616865",
    "data": {
        "id": "1085927476972224522",
        "name": "rolemenu",
        "options": [{"name": "create", "options": [], "type": 1}],
        "type": 1,
    },
    "entitlement_sku_ids": [],
    "guild_id": "882441738713718815",
    "guild_locale": "en-US",
    "id": "1086223588555751514",
    "locale": "en-GB",
    "member": {
        "avatar": None,
        "communication_disabled_until": None,
        "deaf": False,
        "flags": 0,
        "is_pending": False,
        "joined_at": "2023-02-02T15:47:56.859000+00:00",
        "mute": False,
        "nick": None,
        "pending": False,
        "permissions": "4398046511103",
        "premium_since": None,
        "roles": ["1070758821573693624", "1071341486702088193", "1071340327287390248"],
        "user": {
            "avatar": "f7f2e9361e8a54ce6e72580ac7b967af",
            "avatar_decoration": None,
            "discriminator": "3299",
            "display_name": None,
            "id": "1070349326884290602",
            "public_flags": 0,
            "username": "Pranoy",
        },
    },
    "token": "aW50ZXJhY3Rpb246MTA4NjIyMzU4ODU1NTc1MTUxNDpPTnhNSEk3VEhFVTg4TXNIRU05aVNFOGhmdXhmWFZHQVNBaXhiVW0xcmtYMUFIS0o0VmJlbTI5c0I3WklYMGx2amFMdzBwa1JyWWFjYzhaWUJESlNvbmI1MXlhSjhLQkwzWXJPdEdkNExjOUpMR0ZVcVRaeGVScGlxbDVTcG1FeQ",
    "type": 2,
    "version": 1,
}
witho = {
    "app_permissions": "4398046511103",
    "application_id": "1071851326234951770",
    "channel_id": "1070755073866616865",
    "data": {
        "id": "1085927476972224522",
        "name": "rolemenu",
        "options": [
            {
                "name": "delete",
                "options": [
                    {"name": "cname", "type": 3, "value": "hehe"},
                    {"name": "buttons", "type": 3, "value": "B3"},
                ],
                "type": 1,
            }
        ],
        "type": 1,
    },
    "entitlement_sku_ids": [],
    "guild_id": "882441738713718815",
    "guild_locale": "en-US",
    "id": "1086223740074995812",
    "locale": "en-GB",
    "member": {
        "avatar": None,
        "communication_disabled_until": None,
        "deaf": False,
        "flags": 0,
        "is_pending": False,
        "joined_at": "2023-02-02T15:47:56.859000+00:00",
        "mute": False,
        "nick": None,
        "pending": False,
        "permissions": "4398046511103",
        "premium_since": None,
        "roles": ["1070758821573693624", "1071341486702088193", "1071340327287390248"],
        "user": {
            "avatar": "f7f2e9361e8a54ce6e72580ac7b967af",
            "avatar_decoration": None,
            "discriminator": "3299",
            "display_name": None,
            "id": "1070349326884290602",
            "public_flags": 0,
            "username": "Pranoy",
        },
    },
    "token": "aW50ZXJhY3Rpb246MTA4NjIyMzc0MDA3NDk5NTgxMjpKTWdnM3lkOVdudG9sWTloSHJCdDJmMFd5eE44Q2ltWXZ5QmhqbVo0TmhjZWc5RElHTzJpdjE5VXY1cGdlYkF2ZGJIQU9IMElnUXE0RnFaNUhkM3dGMEJoZ0FPM0plR1RlMEl1MHBNZzRudE1NNnYwUkQ1eFhkNm9xYXNKMGd5cA",
    "type": 2,
    "version": 1,
}

more_complezx = {
    "app_permissions": "4398046511103",
    "application_id": "1071851326234951770",
    "channel_id": "1070755073866616865",
    "data": {
        "id": "1085927476972224522",
        "name": "rolemenu",
        "options": [
            {
                "name": "create",
                "options": [{"name": "something", "options": [], "type": 1}],
                "type": 2,
            }
        ],
        "type": 1,
    },
    "entitlement_sku_ids": [],
    "guild_id": "882441738713718815",
    "guild_locale": "en-US",
    "id": "1086228667312644146",
    "locale": "en-GB",
    "member": {
        "avatar": None,
        "communication_disabled_until": None,
        "deaf": False,
        "flags": 0,
        "is_pending": False,
        "joined_at": "2023-02-02T15:47:56.859000+00:00",
        "mute": False,
        "nick": None,
        "pending": False,
        "permissions": "4398046511103",
        "premium_since": None,
        "roles": ["1070758821573693624", "1071341486702088193", "1071340327287390248"],
        "user": {
            "avatar": "f7f2e9361e8a54ce6e72580ac7b967af",
            "avatar_decoration": None,
            "discriminator": "3299",
            "display_name": None,
            "id": "1070349326884290602",
            "public_flags": 0,
            "username": "Pranoy",
        },
    },
    "token": "aW50ZXJhY3Rpb246MTA4NjIyODY2NzMxMjY0NDE0NjoyNFB1UXhsRDQ4NGdzVHVubmlOWDJOSXAySlc4TDBLM2FLWnJkVkxFaGNmTUR0bzFBUEZpMjMzSGU3UGpmZ25HeDNBZ1BBWHlqZWJoaGFrelBtUG5CMFVsMjBQUmNGRDJQbEttVWg0c2dzcVZpc0E1eTRCdTZ6amI4dmZFNU5YTw",
    "type": 2,
    "version": 1,
}
