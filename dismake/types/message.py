from __future__ import annotations

from typing import TYPE_CHECKING, Any, List, Optional, Sequence, TypedDict, Union
from typing_extensions import NotRequired

if TYPE_CHECKING:
    from .user import UserData
    from .snowflake import Snowflake
    from .embed import EmbedData


__all__: Sequence[str] = ("MessageData",)


class MessageData(TypedDict):
    id: Snowflake
    channel_id: Snowflake
    author: UserData
    content: str
    timestamp: str
    edited_timestamp: Optional[str]
    tts: bool
    mention_everyone: bool
    mentions: List[UserData]
    mention_roles: List[Snowflake]
    mention_channels: NotRequired[List[Any]]  # TODO
    attachments: List[Any]  # TODO
    embeds: List[EmbedData]
    reactions: NotRequired[List[Any]]  # TODO
    nonce: NotRequired[Union[str, int]]
    pinned: bool
    webhook_id: NotRequired[Snowflake]
    type: int
    activity: NotRequired[Any]  # TODO
    application: NotRequired[Any]  # TODO
    application_id: NotRequired[Any]  # TODO
    message_reference: NotRequired[Any]  # TODO
    flags: NotRequired[Any]  # TODO
    referenced_message: NotRequired[Optional[Any]]  # TODO
    interaction: NotRequired[Any]  # TODO
    thread: NotRequired[Any]  # TODO
    components: NotRequired[List[Any]]  # TODO
    sticker_items: NotRequired[List[Any]]  # TODO
    stickers: NotRequired[List[Any]]  # TODO
    position: NotRequired[int]
    role_subscription_data: NotRequired[Any]
