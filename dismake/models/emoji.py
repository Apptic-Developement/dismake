from __future__ import annotations

import re
from typing import Optional
from pydantic import BaseModel
from ..types import SnowFlake
from .user import User



__all__ = (
    "Emoji",
    "PartialEmoji"
)

class PartialEmoji(BaseModel):
    id: Optional[SnowFlake]
    name: Optional[str]
    animated: Optional[bool]

    @classmethod
    def from_str(cls, value: str):
        CUSTOM_EMOJI_RE = re.compile(r'<?(?P<animated>a)?:?(?P<name>[A-Za-z0-9\_]+):(?P<id>[0-9]{13,20})>?')
        match = CUSTOM_EMOJI_RE.match(value)
        if match is not None:
            groups = match.groupdict()
            animated = bool(groups["animated"])
            id = int(groups["id"])
            name = groups['name']
            return cls(id=id, name=name, animated=animated)
        return cls(id=None, name=None, animated=None)

        

class Emoji(BaseModel):
    roles: Optional[list[int]]
    user: Optional[User]
    require_colons: Optional[bool]
    managed: Optional[bool]
    available: Optional[bool]