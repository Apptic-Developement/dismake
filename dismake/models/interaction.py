from __future__ import annotations

from enum import IntEnum
from typing import (
    TYPE_CHECKING,
    Any,
    Generic,
    Optional,
    Sequence,
    Tuple,
    Union,
)

from dismake.utils import get_as_snowflake
from .member import Member
from .user import User
from .message import Message
from ..types import ClientT

if TYPE_CHECKING:
    from ..types import InteractionData, Snowflake


__all__: Sequence[str] = ("Interaction",)



class InteractionType(IntEnum):
    PING = 1
    APPLICATION_COMMAND = 2
    MESSAGE_COMPONENT = 3
    APPLICATION_COMMAND_AUTOCOMPLETE = 4
    MODAL_SUBMIT = 5


class Interaction(Generic[ClientT]):
    """Represents a Discord interaction.

    An interaction happens when a user does an action that needs to
    be notified. Current examples are slash commands and components.

    Attributes
    -----------
    id: int
        The interaction's ID.
    type: InteractionType
        The interaction type.
    guild_id: Optional[int]
        The guild ID the interaction was sent from.
    channel: Optional[Any]
        The channel the interaction was sent from.
    application_id: int
        The application ID that the interaction was for.
    user: Union[User, Member]
        The user or member that sent the interaction.
    message: Optional[Message]
        The message that sent this interaction.
        This is only available for :attr:`InteractionType.component` interactions.
    token: str
        The token to continue the interaction. These are valid
        for 15 minutes.
    data: dict
        The raw interaction data.
    locale: Locale
        The locale of the user invoking the interaction.
    guild_locale: Optional[Locale]
        The preferred locale of the guild the interaction was sent from, if any.
    """

    __slots__: Tuple[str, ...] = (
        "_client",
        "data",
        "id",
        "type",
        "application_id",
        "guild_id",
        "channel",
        "channel_id",
        "token",
        "version",
        "app_permissions",
        "locale",
        "guild_locale",
        "message",
        "user",
        "_responded",
    )

    def __init__(self, client: ClientT, data: InteractionData) -> None:
        self._client = client
        self.data = data
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

        self.message: Optional[Message] = (
            Message(client=client, data=data["message"]) if "message" in data else None
        )

        self.user: Optional[Union[User, Member]] = (
            Member(client=client, data=data["member"])
            if self.guild_id is not None and "member" in data
            else User(client=client, data=data["user"])
            if "user" in data
            else None
        )

        self._responded: bool = False

    @property
    def is_ping(self) -> bool:
        """Indicates whether this interaction is a Ping Interaction."""
        return self.type == InteractionType.PING

    @property
    def is_application_command(self) -> bool:
        """Indicates whether this interaction is an Application Command Interaction."""
        return self.type == InteractionType.APPLICATION_COMMAND

    @property
    def is_message_component(self) -> bool:
        """Indicates whether this interaction is a Message Component Interaction."""
        return self.type == InteractionType.MESSAGE_COMPONENT

    @property
    def is_autocomplete(self) -> bool:
        """Indicates whether this interaction is a Application Command Autocomplete Interaction."""
        return self.type == InteractionType.APPLICATION_COMMAND_AUTOCOMPLETE

    @property
    def is_modal_submit(self) -> bool:
        """Indicates whether this interaction is a Modal submit Interaction."""
        return self.type == InteractionType.MODAL_SUBMIT

    @property
    def is_responded(self) -> bool:
        """Indicates whether this interaction is responded."""
        return self._responded
