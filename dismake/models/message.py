from __future__ import annotations

from typing import Any, List, Union, Optional
from datetime import datetime
from pydantic import BaseModel

from .embed import Embed

from ..types import SnowFlake
from .user import User
from ..interaction import Interaction



class Message(BaseModel):
    type: int
    id: SnowFlake
    channel_id: SnowFlake
    author: User
    content: str
    timestamp: datetime
    tts: bool
    mention_everyone: bool
    mentions: List[User]
    mention_roles: List[Any]
    pinned: bool
    edited_timestamp: Optional[datetime]
    mention_channels: Optional[List[Any]]
    attachments: Optional[List[Any]]
    embeds: Optional[List[Embed]]
    reactions: Optional[List[Any]]
    nonce: Optional[Union[str, int]]
    webhook_id: Optional[SnowFlake]
    activity: Optional[Any]
    application: Optional[Any]
    application_id: Optional[Any]
    message_reference: Optional[Any]
    flags: Optional[Any]
    referenced_message: Optional[Any]
    interaction: Optional[Interaction]
    thread: Optional[Any]
    components: Optional[List[Any]]
    sticker_items: Optional[List[Any]]
    stickers: Optional[List[Any]]
    position: Optional[int]
    role_subscription_data: Optional[Any]