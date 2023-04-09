from __future__ import annotations

from typing import Any, List, Optional, TYPE_CHECKING, Union
from fastapi import Request
from pydantic import BaseModel

from dismake.builders.command import Option
from .types import SnowFlake
from .enums import InteractionResponseType, InteractionType, MessageFlags, OptionType
from .models import Member, User
from .params import handle_send_params

if TYPE_CHECKING:
    from .client import Bot
    from .builders import SlashCommandBuilder

__all__ = ("Interaction", "CommandInteraction")


class ResolvedData(BaseModel):
    users: Optional[Any]
    members: Optional[Any]
    channels: Optional[Any]
    roles: Optional[Any]
    messages: Optional[Any]
    attachments: Optional[Any]


class ApplicationCommandOption(BaseModel):
    name: str
    type: int
    value: Optional[Union[str, int, float, bool]]
    options: Optional[List[ApplicationCommandOption]]
    focused: Optional[bool]


class ApplicationCommandData(BaseModel):
    id: SnowFlake
    name: str
    type: int
    resolved: Optional[ResolvedData]
    options: Optional[List[ApplicationCommandOption]]
    guild_id: Optional[SnowFlake]
    target_id: Optional[SnowFlake]


class MessageComponentData(BaseModel):
    custom_id: str
    component_type: int
    # values?*	array of select option values	values the user selected in a select menu component


class ModalSubmitData(BaseModel):
    custom_id: str
    # components	array of message components	the values submitted by the user


class Interaction(BaseModel):
    request: Request
    id: SnowFlake
    application_id: SnowFlake
    type: int
    data: Optional[Union[ApplicationCommandData, MessageComponentData, ModalSubmitData]]
    guild_id: Optional[SnowFlake]
    channel: Optional[Any]
    channel_id: Optional[SnowFlake]
    member: Optional[Member]
    user: Optional[User]
    token: str
    version: int
    message: Optional[Any]
    app_permissions: Optional[str]
    locale: Optional[str]
    guild_locale: Optional[str]

    @property
    def bot(self) -> Bot:
        return self.request.app

    class Config:
        arbitrary_types_allowed = True


class CommandInteraction(Interaction):
    data: Optional[ApplicationCommandData]
    _responded: bool = False

    async def respond(
        self, content: str, *, tts: bool = False, ephemeral: bool = False
    ):
        await self.request.app._http.client.request(
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
        self._responded = True

    async def defer(self, thinking: bool = True):
        await self.request.app._http.client.request(
            method="POST",
            url=f"/interactions/{self.id}/{self.token}/callback",
            json={
                "type": InteractionResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE.value,
                "data": {"flags": MessageFlags.LOADING.value} if not thinking else None,
            },
            headers=self.request.app._http.headers,
        )
        self._responded = True

    async def send_followup(
        self, content: str, *, tts: bool = False, ephemeral: bool = False
    ):
        return await self.request.app._http.client.request(
            method="POST",
            url=f"/webhooks/{self.application_id}/{self.token}",
            json=handle_send_params(content=content, tts=tts, ephemeral=ephemeral),
            headers=self.request.app._http.headers,
        )

    async def send(self, content: str, *, tts: bool = False, ephemeral: bool = False):
        if self._responded:
            return await self.send_followup(content, tts=tts, ephemeral=ephemeral)

        return await self.respond(content, tts=tts, ephemeral=ephemeral)

    @property
    def command(self) -> Optional[SlashCommandBuilder]:
        assert self.data is not None
        return self.bot.get_command(self.data.name)

    @property
    def namespace(self) -> Namespace:
        kwargs = {}
        if (data := self.data) is None or (options := data.options) is None:
            return Namespace()

        opts: Optional[List[ApplicationCommandOption]] = list()
        for option in options:
            if o_opts := option.options:
                for o_opt in o_opts:
                    opts.append(o_opt)

            opts.append(option)
        if not opts:
            return Namespace()
        for opt in opts:
            if opt.type in (OptionType.SUB_COMMAND, OptionType.SUB_COMMAND_GROUP):
                kwargs[opt.name] = True
            else:
                kwargs[opt.name] = opt.value
        return Namespace(**kwargs)


class Namespace:
    def __init__(self, **kwargs):
        for k, v in kwargs.items():
            self.__dict__[k] = v

    def __getattr__(self, attr: str):
        return Namespace()
