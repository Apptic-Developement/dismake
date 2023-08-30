from __future__ import annotations

from typing import TYPE_CHECKING, Any, Optional, Sequence, TypedDict, Dict, List, Union

if TYPE_CHECKING:
    from .user import UserData
    from .snowflake import Snowflake
    from .embed import EmbedData



__all__: Sequence[str] = (
    "MessageData",
)


class MessageData(TypedDict):
    id: int
    channel_id: int
    author: UserData
    content: Optional[str]
    timestamp: str
    edited_timestamp: Optional[str]
    tts: bool
    mention_everyone: bool
    mentions: List[UserData]
    mention_roles: List[Snowflake]
    mention_channels: Optional[List[Dict[Any, Any]]]  # Replace with a more specific type if available
    attachments: List[Dict[Any, Any]]  # Replace with a more specific type if available
    embeds: List[EmbedData]
    reactions: Optional[List[Dict[Any, Any]]]  # Replace with a more specific type if available
    nonce: Optional[Union[int, str]]
    pinned: bool
    webhook_id: Optional[int]
    type: int
    activity: Optional[Dict[Any, Any]]  # Replace with a more specific type if available
    application: Optional[Dict[Any, Any]]  # Replace with a more specific type if available
    application_id: Optional[int]
    message_reference: Optional[Dict[Any, Any]]  # Replace with a more specific type if available
    flags: Optional[int]
    referenced_message: Optional[Dict[Any, Any]]  # Replace with a more specific type if available
    interaction: Optional[Dict[Any, Any]]  # Replace with a more specific type if available
    thread: Optional[Dict[Any, Any]]  # Replace with a more specific type if available
    components: Optional[List[Dict[Any, Any]]]  # Replace with a more specific type if available
    sticker_items: Optional[List[Dict[Any, Any]]]  # Replace with a more specific type if available
    stickers: Optional[List[Dict[Any, Any]]]  # Replace with a more specific type if available
    position: Optional[int]
    role_subscription_data: Optional[Dict[Any, Any]]  # Replace with a more specific type if available