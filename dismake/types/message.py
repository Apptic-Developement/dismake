from __future__ import annotations

import typing



if typing.TYPE_CHECKING:
    from .user import UserData
    from .snowflake import Snowflake
    from .embed import EmbedData
__all__: typing.Sequence[str] = (
    "MessageData",
)


class MessageData(typing.TypedDict):
    id: int
    channel_id: int
    author: UserData
    content: typing.Optional[str]
    timestamp: str
    edited_timestamp: typing.Optional[str]
    tts: bool
    mention_everyone: bool
    mentions: typing.List[UserData]
    mention_roles: typing.List[Snowflake]
    mention_channels: typing.Optional[typing.List[typing.Dict[typing.Any, typing.Any]]]  # Replace with a more specific type if available
    attachments: typing.List[typing.Dict[typing.Any, typing.Any]]  # Replace with a more specific type if available
    embeds: typing.List[EmbedData]
    reactions: typing.Optional[typing.List[typing.Dict[typing.Any, typing.Any]]]  # Replace with a more specific type if available
    nonce: typing.Optional[typing.Union[int, str]]
    pinned: bool
    webhook_id: typing.Optional[int]
    type: int
    activity: typing.Optional[typing.Dict[typing.Any, typing.Any]]  # Replace with a more specific type if available
    application: typing.Optional[typing.Dict[typing.Any, typing.Any]]  # Replace with a more specific type if available
    application_id: typing.Optional[int]
    message_reference: typing.Optional[typing.Dict[typing.Any, typing.Any]]  # Replace with a more specific type if available
    flags: typing.Optional[int]
    referenced_message: typing.Optional[typing.Dict[typing.Any, typing.Any]]  # Replace with a more specific type if available
    interaction: typing.Optional[typing.Dict[typing.Any, typing.Any]]  # Replace with a more specific type if available
    thread: typing.Optional[typing.Dict[typing.Any, typing.Any]]  # Replace with a more specific type if available
    components: typing.Optional[typing.List[typing.Dict[typing.Any, typing.Any]]]  # Replace with a more specific type if available
    sticker_items: typing.Optional[typing.List[typing.Dict[typing.Any, typing.Any]]]  # Replace with a more specific type if available
    stickers: typing.Optional[typing.List[typing.Dict[typing.Any, typing.Any]]]  # Replace with a more specific type if available
    position: typing.Optional[int]
    role_subscription_data: typing.Optional[typing.Dict[typing.Any, typing.Any]]  # Replace with a more specific type if available