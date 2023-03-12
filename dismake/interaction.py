from __future__ import annotations
from typing import Any, Optional
from fastapi import Request
from .types import SnowFlake
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
    def user(self) -> Optional[User]:
        return self._user

    @property
    def member(self) -> Optional[Member]:
        return self._member

    @classmethod
    def _from_app_command(cls, request: Request, data: InteractionData):
        return cls(request=request, data=data)
