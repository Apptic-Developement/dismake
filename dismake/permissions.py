from __future__ import annotations

from enum import IntFlag
from typing import Any

__all__ = ("Permissions",)


class Permissions(IntFlag):
    CREATE_INSTANT_INVITE = 1 << 0  # Allows creation of instant invites (T, V, S)
    KICK_MEMBERS = 1 << 1  # Allows kicking members
    BAN_MEMBERS = 1 << 2  # Allows banning members
    ADMINISTRATOR = (
        1 << 3
    )  # Allows all permissions and bypasses channel permission overwrites
    MANAGE_CHANNELS = 1 << 4  # Allows management and editing of channels (T, V, S)
    MANAGE_GUILD = 1 << 5  # Allows management and editing of the guild
    ADD_REACTIONS = 1 << 6  # Allows for the addition of reactions to messages (T, V, S)
    VIEW_AUDIT_LOG = 1 << 7  # Allows for viewing of audit logs
    PRIORITY_SPEAKER = (
        1 << 8
    )  # Allows for using priority speaker in a voice channel (V)
    STREAM = 1 << 9  # Allows the user to go live (V, S)
    VIEW_CHANNEL = (
        1 << 10
    )  # Allows guild members to view a channel, which includes reading messages in text channels and joining voice channels (T, V, S)
    SEND_MESSAGES = (
        1 << 11
    )  # Allows for sending messages in a channel and creating threads in a forum (does not allow sending messages in threads) (T, V, S)
    SEND_TTS_MESSAGES = 1 << 12  # Allows for sending of /tts messages (T, V, S)
    MANAGE_MESSAGES = 1 << 13  # Allows for deletion of other users' messages (T, V, S)
    EMBED_LINKS = (
        1 << 14
    )  # Links sent by users with this permission will be auto-embedded (T, V, S)
    ATTACH_FILES = 1 << 15  # Allows for uploading images and files (T, V, S)
    READ_MESSAGE_HISTORY = 1 << 16  # Allows for reading of message history (T, V, S)
    MENTION_EVERYONE = (
        1 << 17
    )  # Allows for using the @everyone tag to notify all users in a channel, and the @here tag to notify all online users in a channel (T, V, S)
    USE_EXTERNAL_EMOJIS = (
        1 << 18
    )  # Allows the usage of custom emojis from other servers (T, V, S)
    VIEW_GUILD_INSIGHTS = 1 << 19  # Allows for viewing guild insights
    CONNECT = 1 << 20  # Allows for joining of a voice channel (V, S)
    SPEAK = 1 << 21  # Allows for speaking in a voice channel (V)
    MUTE_MEMBERS = 1 << 22  # Allows for muting members in a voice channel (V, S)
    DEAFEN_MEMBERS = 1 << 23  # Allows for deafening of members in a voice channel (V)
    MOVE_MEMBERS = 1 << 24  # Allows for moving of members between voice channels (V, S)
    USE_VAD = (
        1 << 25
    )  # Allows for using voice-activity-detection in a voice channel (V)
    CHANGE_NICKNAME = 1 << 26  # Allows for modification of own nickname
    MANAGE_NICKNAMES = 1 << 27  # Allows for modification of other users' nicknames

    @classmethod
    def _missing_(cls, value: object) -> Any:
        if isinstance(value, str):
            if value.isdigit():
                return super()._missing_(int(value))
