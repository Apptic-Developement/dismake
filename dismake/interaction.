from __future__ import annotations
from typing import Any, Optional
from fastapi import Request

from pydantic import BaseModel


from .params import handle_send_params
from .enums import InteractionResponseType
from .types import SnowFlake
from .models import Member
from .enums import MessageFlags


__all__ = ("Interaction", "CommandData", "ComponentData")


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
    value: Optional[str | int | float]
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


make = {
    "app_permissions": "4398046511103",
    "application_id": "1071851326234951770",
    "channel_id": "1070755073866616865",
    "data": {
        "id": "1085031408583573594",
        "name": "hello",
        "options": [{"name": "name", "type": 3, "value": "Pranoy"}],
        "type": 1,
    },
    "entitlement_sku_ids": [],
    "guild_id": "882441738713718815",
    "guild_locale": "en-US",
    "id": "1085031928484339762",
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
    "token": "aW50ZXJhY3Rpb246MTA4NTAzMTkyODQ4NDMzOTc2Mjp6bVpXdk1vNGpMMXppelpVWjM0dXp6c0t5VTBIYWdhTWIxTzJlckdwQUFCektsRzJ3Z1VudTB1YWRzR1hMMzZzdzRRdWRnWjJXZVV5eGliYlNpUEx4RFZZR2t0MTBZeGx1WXJJV2RicG5SNDU4RzlnVlFyYjI5ampzNThQRGJaeA",
    "type": 2,
    "version": 1,
}


class Interaction(BaseModel):
    request: Request
    type: int
    token: str
    member: Optional[Member]
    id: SnowFlake
    application_id: SnowFlake
    guild_id: SnowFlake
    app_permissions: str
    guild_locale: Optional[str]
    locale: Optional[str]
    data: CommandData
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
