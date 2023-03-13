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
    application_id: SnowFlake
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
        if not self._responded:
            return await self.request.app._http.client.request(
                method="POST",
                url=f"/interactions/{self.id}/{self.token}/callback",
                json={
                    "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE.value,
                    "data": {"content": content, "tts": tts},
                },
                headers=self.request.app._http.headers,
            )
        return await self.send_followup(content, tts=tts, ephemeral=ephemeral)

    async def defer(self, thinking: bool = True):
        return await self.request.app._http.client.request(
            method="POST",
            url=f"/interactions/{self.id}/{self.token}/callback",
            json={
                "type": InteractionResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE.value,
                "data": {"thinking": thinking},
            },
            headers=self.request.app._http.headers,
        )

    async def send_followup(
        self, content: str, *, tts: bool = False, ephemeral: bool = False
    ):

        return await self.request.app._http.client.request(
            method="POST",
            url=f"/webhooks/{self.application_id}/{self.token}",
            json={"content": content, "tts": tts},
            headers=self.request.app._http.headers,
        )


    class Config:
        arbitrary_types_allowed = True


