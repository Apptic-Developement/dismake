from pydantic import BaseModel
from typing import Dict, List, Optional, Union
from ..types import SnowFlake


__all__ = (
    "ApplicationCommandChoice",
    "ApplicationCommandOption",
    "ApplicationCommand",
)


class ApplicationCommandChoice(BaseModel):
    name: str
    value: Union[str, int, float]


class ApplicationCommandOption(BaseModel):
    type: int
    name: str
    name_localizations: Optional[dict[str, str]]
    description: Optional[str] = "No description provided"
    description_localizations: Optional[dict[str, str]]
    required: Optional[bool] = False
    choices: Optional[List[ApplicationCommandChoice]]
    options: Optional[List["ApplicationCommandOption"]]
    channel_types: Optional[List[str]]
    min_value: Optional[int]
    max_value: Optional[int]
    min_length: Optional[int]
    max_length: Optional[int]
    autocomplete: Optional[bool]


class ApplicationCommand(BaseModel):
    id: SnowFlake
    type: int = 1
    application_id: SnowFlake
    guild_id: Optional[SnowFlake]
    name: str
    name_localizations: Optional[Dict[str, str]]
    description: Optional[str] = "No description provided"
    description_localizations: Optional[Dict[str, str]]
    options: Optional[List[ApplicationCommandOption]]
    default_member_permissions: Optional[str]
    dm_permission: Optional[bool] = True
    nsfw: Optional[bool] = False
    version: int
