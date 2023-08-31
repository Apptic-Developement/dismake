from __future__ import annotations

from typing import TYPE_CHECKING, Any, Generic, Optional, Sequence, TypeVar, Union
from enum import IntEnum

from dismake.utils import get_as_snowflake
from .member import Member
from .user import User
from .message import Message

if TYPE_CHECKING:
    from ..client import Client
    from ..types import InteractionData, Snowflake


__all__: Sequence[str] = ("Interaction",)

ClientT = TypeVar("ClientT", bound="Client")


class InteractionType(IntEnum):
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    MODAL_SUBMIT = 5


class Interaction(Generic[ClientT]):
    def __init__(self, client: Client, data: InteractionData) -> None:
        self._client = client
        self.id: int = int(data["id"])
        self.type: InteractionType = InteractionType(int(data["type"]))
        self.application_id: Snowflake = data["application_id"]
        self.guild_id: Optional[int] = get_as_snowflake(data, "guild_id")
        self.channel: Optional[Any] = get_as_snowflake(data, "channel")
        self.channel_id: Optional[int] = get_as_snowflake(data, "channel_id")
        self.token: str = data["token"]
        self.version: int = data["version"]

        self.app_permissions: Optional[str] = data.get("app_permissions")
        self.locale: Optional[str] = data.get("locale")
        self.guild_locale: Optional[str] = data.get("guild_locale")

        self._message = data.get("message")
        self.message: Optional[Message]
        if self._message is not None:
            self.message = Message(client=client, data=self._message)

        self.user: Union[User, Member]
        if self.guild_id is not None and (member := data.get("member")) is not None:
            self.user = Member(client=client, data=member) # TODO
        else:
            self.user = User(client=client, data=data["user"])  # type: ignore

    @property
    def is_ping(self) -> bool:
        return self.type == InteractionType.PING

    @property
    def is_application_command(self) -> bool:
        return self.type == InteractionType.APPLICATION_COMMAND

    @property
    def is_message_component(self) -> bool:
        return self.type == InteractionType.MESSAGE_COMPONENT

    @property
    def is_autocomplete(self) -> bool:
        return self.type == InteractionType.APPLICATION_COMMAND_AUTOCOMPLETE

    @property
    def is_modal_submit(self) -> bool:
        return self.type == InteractionType.MODAL_SUBMIT
