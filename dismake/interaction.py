from __future__ import annotations

from typing import Any, List, Optional, TYPE_CHECKING, Union
from fastapi import Request
from pydantic import BaseModel
from .types import SnowFlake
from .enums import InteractionType, OptionType
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

    @property
    def command(self) -> Optional[SlashCommandBuilder]:
        assert self.data is not None
        return self.bot.get_command(self.data.name)

    def get_string(self, string: str):
        assert self.data is not None
        if not (options := self.data.options):
            return None
        opts = list(
            filter(
                lambda option: option.name == string
                and option.type == OptionType.STRING,
                options,
            )
        )
        if opts:
            return opts[0].value
