from __future__ import annotations

from typing import Optional

from pydantic import BaseModel
from ..types import SnowFlake

__all__ = ("PartialMessagable", "TextChannel")


class PartialMessagable(BaseModel):
    id: SnowFlake


class CategoryChannel(PartialMessagable):
    ...


class TextChannel(PartialMessagable):
    ...
