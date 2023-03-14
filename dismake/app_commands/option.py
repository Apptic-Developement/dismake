from __future__ import annotations
from typing import Optional
from pydantic import BaseModel, validator


from ..enums import OptionType
from .base import BaseSlashCommand
__all__ = ("Choice", "Option")



class Choice(BaseModel):
    name: str
    value: str | int | float


class Option(BaseSlashCommand):
    type: int = OptionType.STRING
    name: str
    description: str
    name_localizations: Optional[dict[str, str]] = None
    description_localizations: Optional[dict[str, str]] = None
    required: bool = False
    choices: Optional[list[Choice]] = None
    options: Optional[list[Option]] = None
    # channel_types: Optional[ChannelTypes] = None
    min_value: Optional[int] = None
    max_value: Optional[int] = None
    min_length: Optional[int] = None
    max_length: Optional[int] = None
    autocomplete: Optional[bool] = None

    @validator("min_length")
    def validate_min_length(cls, value: int):
        if value < 0 or value > 6000:
            raise ValueError(
                "For option type STRING, the minimum allowed length (minimum of 0, maximum of 6000)"
            )
        return value

    @validator("max_length")
    def validate_max_length(cls, value: int):
        if value < 1 or value > 6000:
            raise ValueError(
                "For option type STRING, the maximum allowed length (minimum of 1, maximum of 6000)"
            )
        return value

    @validator("type")
    def validate_type(cls, value: int):
        if value in (OptionType.SUB_COMMAND, OptionType.SUB_COMMAND_GROUP):
            raise TypeError(
                "You can not use SUB_COMMAND or SUB_GROUP type in command option."
            )
        return value

