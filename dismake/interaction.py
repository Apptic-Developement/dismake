from __future__ import annotations
from typing import Optional
from fastapi import Request
from .models import Interaction as InteractionData
from .models import User, Member

__all__ = ("Interaction",)


class Interaction:
    def __init__(self, request: Request, data: InteractionData):
        self._request = request
        self._id = data.id
        self._application_id = data.application_id
        self._type = data.type
        self._data = data.data
        self._guild_id = data.guild_id
        self._channel_id = data.channel_id
        self._member = data.member
        self._user = data.user
        self._token = data.token
        self._version = data.version
        self._message = data.message
        self._app_permissions = data.app_permissions
        self._locale = data.locale
        self._guild_locale = data.guild_locale

    @property
    def user(self) -> User:
        return self._user

    @property
    def member(self) -> Optional[Member]:
        return self._member

    @classmethod
    def _from_app_command(cls, request: Request, data: InteractionData):
        return cls(request=request, data=data)


make = {
    "app_permissions": "4398046511103",
    "application_id": "1071851326234951770",
    "channel_id": "1050631408693030973",
    "data": {
        "id": "1084106102708375653",
        "name": "ping",
        "options": [{"name": "sub", "options": [], "type": 1}],
        "type": 1,
    },
    "entitlement_sku_ids": [],
    "guild_id": "1047495912089473054",
    "guild_locale": "en-US",
    "id": "1084504735874285742",
    "locale": "en-GB",
    "member": {
        "avatar": None,
        "communication_disabled_until": None,
        "deaf": False,
        "flags": 0,
        "is_pending": False,
        "joined_at": "2022-11-30T12:54:47.035000+00:00",
        "mute": False,
        "nick": None,
        "pending": False,
        "permissions": "4398046511103",
        "premium_since": None,
        "roles": [
            "1057154747339128902",
            "1057154942281982055",
            "1057154857166979082",
            "1057154822266179695",
            "1057154622776688720",
            "1057154666250641488",
            "1057154900716441743",
            "1057154978457866291",
            "1047852687405895700",
            "1066238596190834708",
            "1057154781145215038",
            "1057154715193983007",
        ],
        "user": {
            "avatar": "94de12ce96deb607397ade18d6989ed2",
            "avatar_decoration": None,
            "discriminator": "0140",
            "display_name": None,
            "id": "942683245106065448",
            "public_flags": 4194560,
            "username": "Pranoy",
        },
    },
    "token": "aW50ZXJhY3Rpb246MTA4NDUwNDczNTg3NDI4NTc0MjpHTzczSUZBZWNjdGkzZUo2clkyRkRhVEx0WVM1bmkzU3JJR0kyT3ZSeDJmcWV1SlNDb3hpcVF4SEVJS29WWTZnSEs5eDFRTjk1QjJuUDV4d0FWTkNBdmhSQmp3RVlzMlFIRzBub3luTTlpSHREdWw2dHAxbGFFTWNQbWtZenlUYQ",
    "type": 2,
    "version": 1,
}
