from __future__ import annotations

from typing import Any, List, Optional, TYPE_CHECKING, Union, Dict, TYPE_CHECKING
from fastapi import Request
from pydantic import BaseModel, validator

from .types import SnowFlake
from .models import Member, User, Guild, Message, Role
from .enums import InteractionType, InteractionResponseType, MessageFlags
from .errors import InteractionNotResponded, InteractionResponded, ComponentException
from .params import handle_send_params
if TYPE_CHECKING:
    from .ui import House


if TYPE_CHECKING:
    from .client import Bot

__all__ = ("Interaction", "ApplicationCommandData", "ApplicationCommandOption")


class ResolvedData(BaseModel):
    users: Optional[Dict[str, User]]
    members: Optional[Any]
    channels: Optional[Any]
    roles: Optional[Dict[str, Role]]
    messages: Optional[Any]
    attachments: Optional[Any]


class ApplicationCommandOption(BaseModel):
    name: str
    type: int
    value: Optional[Union[str, int, float, bool, User, Role]]
    options: Optional[List[ApplicationCommandOption]]
    focused: bool = False


class ApplicationCommandData(BaseModel):
    id: SnowFlake
    name: str
    type: int
    resolved: Optional[ResolvedData]
    options: Optional[List[ApplicationCommandOption]]
    guild_id: Optional[SnowFlake]
    target_id: Optional[SnowFlake]



class Interaction(BaseModel):
    request: Request
    is_response_done: bool
    id: SnowFlake
    application_id: SnowFlake
    type: int
    guild_id: Optional[int]
    channel: Optional[Any]
    channel_id: Optional[SnowFlake]
    member: Optional[Member]
    user: Optional[User]
    token: str
    version: int
    message: Optional[Message]
    app_permissions: Optional[str]
    locale: Optional[str]
    guild_locale: Optional[str]

    @property
    def is_responded(self) -> bool:
        return self.is_response_done

    @property
    def is_application_command(self) -> bool:
        return self.type == InteractionType.APPLICATION_COMMAND.value

    @property
    def is_autocomplete(self) -> bool:
        return self.type == InteractionType.APPLICATION_COMMAND_AUTOCOMPLETE.value

    @property
    def is_modal_submit(self) -> bool:
        return self.type == InteractionType.MODAL_SUBMIT.value

    @property
    def is_ping(self) -> bool:
        return self.type == InteractionType.PING.value

    @property
    def is_component(self) -> bool:
        return self.type == InteractionType.MESSAGE_COMPONENT.value

    @property
    def author(self) -> Union[Member, User]:
        if self.guild_id:
            assert self.member is not None
            return self.member
        assert self.user is not None
        return self.user

    async def fetch_guild(self) -> Guild:
        assert self.guild_id is not None, "Guild id is none."
        return await self.bot.fetch_guild(self.guild_id)

    @property
    def bot(self) -> Bot:
        return self.request.app
    
    async def respond(
        self,
        content: str,
        *,
        tts: bool = False,
        ephemeral: bool = False,
        houses: Optional[List[House]] = None,
    ):
        if self.is_responded:
            raise InteractionResponded(self)
        
        if houses:
            if len(houses) > 5:
                raise ComponentException("A message can only have 5 houses.")
            for house in houses:
                self.bot.add_house(house)
        await self.request.app._http.client.request(
            method="POST",
            url=f"/interactions/{self.id}/{self.token}/callback",
            json={
                "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE.value,
                "data": handle_send_params(
                    content=content, tts=tts, ephemeral=ephemeral, houses=houses
                ),
            },
            headers=self.request.app._http.headers,
        )
        self.is_response_done = True

    async def defer(self, thinking: bool = True):
        if self.is_responded:
            raise InteractionResponded(self)
        await self.request.app._http.client.request(
            method="POST",
            url=f"/interactions/{self.id}/{self.token}/callback",
            json={
                "type": InteractionResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE.value,
                "data": {"flags": MessageFlags.LOADING.value} if not thinking else None,
            },
            headers=self.request.app._http.headers,
        )
        self.is_response_done = True

    async def send_followup(
        self, content: str, *, tts: bool = False, houses: Optional[List[House]] = None, ephemeral: bool = False
    ):
        if not self.respond:
            raise InteractionNotResponded(self)
        
        if houses:
            if len(houses) > 5:
                raise ComponentException("A message can only have 5 houses.")
            for house in houses:
                self.bot.add_house(house)
        return await self.request.app._http.client.request(
            method="POST",
            url=f"/webhooks/{self.application_id}/{self.token}",
            json=handle_send_params(content=content, tts=tts, ephemeral=ephemeral),
            headers=self.request.app._http.headers,
        )

    # async def edit_original_response(
    #     self,
    #     content: str
    # ):
    #     return await self.bot._http.client.request(
    #         method="PATCH",
    #         url=f"/webhooks/{self.application_id}/{self.token}/messages/{self.message.id}"
            
    #     )

    async def send(self, content: str, *, tts: bool = False, houses: Optional[List[House]] = None, ephemeral: bool = False):
        if self.is_responded:
            return await self.send_followup(content, tts=tts, houses=houses, ephemeral=ephemeral)
        return await self.respond(content, tts=tts, houses=houses, ephemeral=ephemeral)
    class Config:
        arbitrary_types_allowed = True
