from __future__ import annotations

from typing import TYPE_CHECKING, Any, Dict, List, Optional, Sequence, Union

from .embed import Embed
from .role import PartialRole
from .user import User
from ..utils import parse_time, snowflake_time

if TYPE_CHECKING:
    from dismake import Client
    from dismake.types import MessageData
    from datetime import datetime

__all__: Sequence[str] = (
    "PartialMessage",
    "Message",
)


class PartialMessage:
    def __init__(self, client: Client, id: int) -> None:
        self.id = id
        self.client = client


class Message(PartialMessage):
    def __init__(self, client: Client, data: MessageData) -> None:
        super().__init__(client, id=int(data["id"]))
        self.channel_id: int = int(data["channel_id"])
        self.author: User = User(client=client, data=data["author"])
        self.content: Optional[str] = data.get("content")
        self.edited_timestamp: Optional[datetime] = parse_time(
            data.get("edited_timestamp")
        )
        self.tts: bool = data["tts"]
        self.mention_everyone: bool = data["mention_everyone"]
        self.mentions: List[User] = [
            User(client=client, data=u) for u in data["mentions"]
        ]
        self.mention_roles: List[PartialRole] = [
            PartialRole(client=client, id=int(r)) for r in data["mention_roles"]
        ]
        # self.mention_channels: Channel TODO
        # self.attachments TODO
        self.embeds: List[Embed] = [Embed.from_dict(e) for e in data["embeds"]]
        self.reactions: Optional[List[Dict[Any, Any]]]
        self.nonce: Optional[Union[int, str]]
        self.pinned: bool
        self.webhook_id: Optional[int]
        self.type: int
        self.activity: Optional[Dict[Any, Any]]
        self.application: Optional[Dict[Any, Any]]
        self.application_id: Optional[int]
        self.message_reference: Optional[Dict[Any, Any]]
        self.flags: Optional[int]
        self.referenced_message: Optional[Dict[Any, Any]]
        self.interaction: Optional[Dict[Any, Any]]
        self.thread: Optional[Dict[Any, Any]]
        self.components: Optional[List[Dict[Any, Any]]]
        self.sticker_items: Optional[List[Dict[Any, Any]]]
        self.stickers: Optional[List[Dict[Any, Any]]]
        self.position: Optional[int]
        self.role_subscription_data: Optional[Dict[Any, Any]]

    @property
    def created_at(self) -> datetime:
        """The message's creation time in UTC."""
        return snowflake_time(self.id)
