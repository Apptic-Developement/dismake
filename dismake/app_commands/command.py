from __future__ import annotations
from typing import Optional

from pydantic import BaseModel

from ..types import SnowFlake

from ..enums import CommandType, OptionType


class CommandChoice(BaseModel):
    name: str
    value: str | int | float


class CommandOption(BaseModel):
    name: str
    description: str
    type: int = OptionType.STRING.value
    required: bool = False

class Group(BaseModel):
    name: str

class Command(BaseModel):
    name: str
    description: str
    type: int = CommandType.SLASH.value
    guild_id: SnowFlake
    options: Optional[list[CommandOption]]
