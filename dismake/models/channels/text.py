from __future__ import annotations
from pydantic import BaseModel

# class TextChannel(BaseModel):
#     guild_id: int
#     """ ID of guild were text channel belongs """
#     position: int
#     """ Text channel position """
#     permission_overwrites: Optional[List[PermissionsOverwrite]] = list()
#     """ Channel Permissions """
#     name: str
#     """ Name of channel """
#     topic: Optional[str]
#     """ Channel topic """
#     nsfw: Optional[bool] = False
#     """ Whether channel is marked as NSFW """
#     last_message_id: Optional[int]
#     """ Last message in channel, may or may not be valid """
#     parent_id: Optional[int]
#     """ Category to which the channel belongs to """
#     last_pin_timestamp: Optional[datetime.datetime]
#     """ Last pinned message in channel, may be None """
#     permissions: Optional[str]
#     """ String of user permissions """
#     rate_limit_per_user: Optional[int]
#     """ Channel ratelimit """
#     default_auto_archive_duration: Optional[int]
#     """ Default time for threads to be archived """

#     created_at: Optional[datetime.datetime]
#     """ When this channel was created """