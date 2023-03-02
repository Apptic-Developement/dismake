from __future__ import annotations

from pydantic import BaseModel
from typing import Optional
from ..types import CommandTypes, OptionTypes

__all__ = (
    "Option",
    "Choice",
    "Command"
)
class Option(BaseModel):
    name: str
    description: str = "No Description Provided."
    choices: Optional[list[Choice]] = []
    channel_types: Optional[str]  # TODO: Optional[ChannelTypes]
    min_value: Optional[int]
    max_value: Optional[int]
    min_length: Optional[int]
    max_length: Optional[int]
    required: Optional[bool] = False
    type: Optional[OptionTypes] = OptionTypes.STRING
    autocomplete: Optional[bool] = False


class Choice(BaseModel):
    name: str
    value: str | int | float


class Command(BaseModel):
    name: str
    description: str = "No Description Provided."
    id: Optional[int] = None
    options: list[Option] = []
    default_permission: bool = True
    type: CommandTypes | int = CommandTypes.SLASH

    async def callback(self):
        ...

