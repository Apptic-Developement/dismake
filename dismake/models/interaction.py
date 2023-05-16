from __future__ import annotations
from re import I

from typing import Any, List, Optional, TYPE_CHECKING, Union, Dict, TYPE_CHECKING
from pydantic import BaseModel
from .user import Member, User
from .guild import Guild
from .role import Role
from .message import Message
from ..enums import InteractionType, InteractionResponseType, MessageFlags, OptionType
from ..errors import InteractionNotResponded, InteractionResponded
from ..params import handle_send_params, handle_edit_params
from fastapi import Request
from ..types import SnowFlake
from .channels import Channel
from .components import TextInput

if TYPE_CHECKING:
    from ..ui import View, Modal
    from ..client import Bot
    from ..commands import Choice


__all__ = (
    "Interaction",
    "ApplicationCommandData",
    "ApplicationCommandOption",
    "MessageComponentData",
    "ModalSubmitData",
    "ModalSubmitActionRowData"
)


def _extract_options(
    option: ApplicationCommandOption,
) -> List[ApplicationCommandOption]:
    """Recursively extract options from commands"""
    if option.type == OptionType.SUB_COMMAND.value and option.options is not None:
        return [o for sub_opt in option.options for o in _extract_options(sub_opt)]
    elif (
        option.type == OptionType.SUB_COMMAND_GROUP.value and option.options is not None
    ):
        return [o for sub_group in option.options for o in _extract_options(sub_group)]
    else:
        return [option]


def _options_to_dict(
    options: List[ApplicationCommandOption], resolved_data: Optional[ResolvedData]
) -> Dict[str, Any]:
    """Convert options to a dictionary"""
    namespace_dict = {}
    for option in options:
        if option.type == OptionType.USER.value and resolved_data is not None:
            if resolved_data.users is not None:
                namespace_dict[option.name.replace("-", "_")] = resolved_data.users.get(
                    str(option.value)  # type: ignore
                )
        elif option.type == OptionType.ROLE.value and resolved_data is not None:
            if resolved_data.roles is not None:
                namespace_dict[option.name.replace("-", "_")] = resolved_data.roles.get(
                    str(option.value)  # type: ignore
                )
        elif option.type == OptionType.CHANNEL.value and resolved_data is not None:
            if resolved_data.channels is not None:
                namespace_dict[
                    option.name.replace("-", "_")
                ] = resolved_data.channels.get(
                    str(option.value)
                )  # type: ignore
        else:
            namespace_dict[option.name.replace("-", "_")] = option.value  # type: ignore
    return namespace_dict


class ResolvedData(BaseModel):
    users: Optional[Dict[str, User]]
    members: Optional[Any]
    channels: Optional[Dict[str, Channel]]
    roles: Optional[Dict[str, Role]]
    messages: Optional[Any]
    attachments: Optional[Any]


class ApplicationCommandOption(BaseModel):
    name: str
    type: int
    value: Optional[Union[str, int, float, bool, User, Role, Channel]]
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


class MessageComponentData(BaseModel):
    custom_id: str
    component_type: int
    values: Optional[List[str]]


class ModalSubmitActionRowData(BaseModel):
    components: list[TextInput]


class ModalSubmitData(BaseModel):
    custom_id: str
    components: list[ModalSubmitActionRowData]



class Interaction:
    """
    Represents a Discord interaction.

    An interaction happens when a user does an action that needs to
    be notified. Current examples are slash commands and components.

    Parameters
    -----------
    request: Request
        The request object.
    data: Dict[str, Any]
        The interaction data
    """

    __slots__ = (
        "_request",
        "_is_response_done",
        "id",
        "application_id",
        "type",
        "token",
        "version",
        "guild_id",
        "channel_id",
        "app_permissions",
        "locale",
        "guild_locale",
        "user",
        "_data",
        "data",
        "channel",
        "__message",
        "message",
    )

    def __init__(self, request: Request, data: Dict[str, Any]) -> None:
        self._request = request
        self._is_response_done = False
        self.id: int = int(data["id"])
        self.application_id: SnowFlake = data["application_id"]
        self.type: int = data["type"]
        self.token: str = data["token"]
        self.version: int = data["version"]
        self.guild_id: Optional[int] = data.get("guild_id")
        self.channel_id: Optional[SnowFlake] = data.get("channel_id")
        self.app_permissions: Optional[int] = data.get("app_permissions")
        self.locale: Optional[str] = data.get("locale")
        self.guild_locale: Optional[str] = data.get("guild_locale")
        self.user: Union[User, Member]
        self._data: Optional[dict] = data.get("data")
        self.data: Optional[
            Union[ApplicationCommandData, ModalSubmitData, MessageComponentData]
        ]
        if self.is_application_command or self.is_autocomplete:
            self.data = ApplicationCommandData(**self._data) if self._data else None
        elif self.is_message_component:
            self.data = MessageComponentData(**self._data) if self._data else None
        else:
            self.data = ModalSubmitData(**self._data) if self._data else None
        if self.guild_id:
            try:
                member = data["member"]
            except:
                pass
            else:
                self.user = Member(**member)
        else:
            self.user = User(**data["user"])
        self.channel: Optional[Any] = data.get("channel")
        self.__message: Optional[dict] = data.get("message")
        self.message: Optional[Message]
        if self.__message is not None:
            self.message = Message(_request=self._request, **self.__message)

    @property
    def bot(self) -> Bot:
        """
        :class:`Bot`: The bot that is handling this interaction.
        """
        return self._request.app

    @property
    def is_application_command(self) -> bool:
        """
        The is_application_command function checks if the interaction type is an application command.
        """
        return self.type == InteractionType.APPLICATION_COMMAND.value

    @property
    def is_autocomplete(self) -> bool:
        """
        The is_autocomplete function checks if the interaction type is an autocomplete.
        """
        return self.type == InteractionType.APPLICATION_COMMAND_AUTOCOMPLETE.value

    @property
    def is_modal_submit(self) -> bool:
        """
        The is_modal_submit function checks if the interaction type is a modal submit.
        """
        return self.type == InteractionType.MODAL_SUBMIT.value

    @property
    def is_ping(self) -> bool:
        """
        The is_ping function checks if the interaction type is a ping.
        """
        return self.type == InteractionType.PING.value

    @property
    def is_message_component(self) -> bool:
        """
        The is_component function checks if the interaction is a component.
        """
        return self.type == InteractionType.MESSAGE_COMPONENT.value

    @property
    def is_responded(self) -> bool:
        """
        :class:`bool`: Indicates whether an interaction response has been done before.
        An interaction can only be responded to once.
        """
        return self._is_response_done

    @property
    def namespace(self) -> Namespace:
        if not isinstance(self.data, ApplicationCommandData):
            return Namespace(**{})
        if (data := self.data) is None or (options := data.options) is None:
            return Namespace(**{})

        options = [o for option in options for o in _extract_options(option)]
        if not options:
            return Namespace(**{})

        return Namespace(**_options_to_dict(options, data.resolved))

    async def fetch_guild(self) -> Optional[Guild]:
        """
        This function is a coroutine that returns the Guild object for this interaction.
        It is used to get the guild object from its ID, which is stored in self.guild_id.

        Returns
        -------
        Optional[Guild]:
            A guild object if the guild_id is not none.
        """
        if self.guild_id is None:
            return None
        return await self.bot.fetch_guild(self.guild_id)

    async def respond(
        self,
        content: str,
        *,
        tts: bool = False,
        ephemeral: bool = False,
        view: Optional[View] = None,
    ):
        if self.is_responded:
            raise InteractionResponded(self)

        if view:
            self.bot.add_view(view)
        await self.bot._http.client.request(
            method="POST",
            url=f"/interactions/{self.id}/{self.token}/callback",
            json={
                "type": InteractionResponseType.CHANNEL_MESSAGE_WITH_SOURCE.value,
                "data": handle_send_params(
                    content=content, tts=tts, ephemeral=ephemeral, view=view
                ),
            },
            headers=self.bot._http.headers,
        )
        self._is_response_done = True

    async def defer(self, thinking: bool = True):
        if self.is_responded:
            raise InteractionResponded(self)
        await self.bot._http.client.request(
            method="POST",
            url=f"/interactions/{self.id}/{self.token}/callback",
            json={
                "type": InteractionResponseType.DEFERRED_CHANNEL_MESSAGE_WITH_SOURCE.value,
                "data": {"flags": MessageFlags.LOADING.value} if not thinking else None,
            },
            headers=self.bot._http.headers,
        )
        self._is_response_done = True

    async def send_followup(
        self,
        content: str,
        *,
        tts: bool = False,
        view: Optional[View] = None,
        ephemeral: bool = False,
    ):
        if not self.is_responded:
            raise InteractionNotResponded(self)

        if view:
            self.bot.add_view(view)
        return await self.bot._http.client.request(
            method="POST",
            url=f"/webhooks/{self.application_id}/{self.token}",
            json=handle_send_params(
                content=content, tts=tts, view=view, ephemeral=ephemeral
            ),
        )

    async def edit_original_response(
        self, content: str, *, tts: bool = False, view: Optional[View] = None
    ):
        if view:
            self.bot.add_view(view)
        return await self.bot._http.client.request(
            method="PATCH",
            url=f"/webhooks/{self.application_id}/{self.token}/messages/@original",
            json=handle_edit_params(content=content, tts=tts, view=view),
        )

    async def get_original_response(self) -> Message:
        res = await self.bot._http.client.request(
            method="GET",
            url=f"/webhooks/{self.application_id}/{self.token}/messages/@original",
        )
        res.raise_for_status()
        return Message(**res.json())

    async def send(
        self,
        content: str,
        *,
        tts: bool = False,
        view: Optional[View] = None,
        ephemeral: bool = False,
    ):
        if self.is_responded:
            return await self.send_followup(
                content, tts=tts, view=view, ephemeral=ephemeral
            )
        return await self.respond(content, tts=tts, view=view, ephemeral=ephemeral)

    async def edit_message(
        self, content: str, *, tts: bool = False, view: Optional[View] = None
    ):
        if not self.is_message_component:
            return
        if self.is_responded:
            raise InteractionResponded(self)
        if view:
            self.bot.add_view(view)
        payload = handle_edit_params(content=content, tts=tts, view=view)
        return await self.bot._http.client.request(
            method="POST",
            url=f"/interactions/{self.id}/{self.token}/callback",
            json={
                "type": InteractionResponseType.UPDATE_MESSAGE.value,
                "data": payload,
            },
        )

    async def autocomplete(self, choices: List[Choice]):
        if not self.is_autocomplete:
            return

        return await self.bot._http.client.request(
            method="POST",
            url=f"/interactions/{self.id}/{self.token}/callback",
            json={
                "type": InteractionResponseType.APPLICATION_COMMAND_AUTOCOMPLETE_RESULT.value,
                "data": {"choices": [choice.to_dict() for choice in choices]},
            },
        )

    async def respond_with_modal(self, modal: Modal):
        if self.is_responded:
            raise InteractionResponded(self)
        self.bot.add_modal(modal)
        return await self.bot._http.client.request(
            method="POST",
            url=f"/interactions/{self.id}/{self.token}/callback",
            json={"type": InteractionResponseType.MODAL.value, "data": modal.to_dict()},
        )


class Namespace:
    """
    Inspired from discord.py
    """

    def __init__(self, **kwargs) -> None:
        for k, v in kwargs.items():
            self.__dict__[k] = v

    def __getattr__(self, value) -> None:
        return None
