from pydantic import BaseModel
from typing import Dict, List, Optional, Union
from ..types import SnowFlake


__all__ = (
    "AppCommandChoice",
    "AppCommandOption",
    "AppCommand",
)


class AppCommandChoice(BaseModel):
    name: str
    value: Union[str, int, float]


class AppCommandOption(BaseModel):
    type: int
    name: str
    name_localizations: Optional[Dict[str, str]]
    description: Optional[str] = "No description provided"
    description_localizations: Optional[Dict[str, str]]
    required: Optional[bool] = False
    choices: Optional[List[AppCommandChoice]]
    options: Optional[List["AppCommandOption"]]
    channel_types: Optional[List[str]]
    min_value: Optional[int]
    max_value: Optional[int]
    min_length: Optional[int]
    max_length: Optional[int]
    autocomplete: Optional[bool]


class AppCommand(BaseModel):
    id: SnowFlake
    type: int = 1
    App_id: SnowFlake
    guild_id: Optional[SnowFlake]
    name: str
    name_localizations: Optional[Dict[str, str]]
    description: Optional[str] = "No description provided"
    description_localizations: Optional[Dict[str, str]]
    options: Optional[List[AppCommandOption]]
    default_member_permissions: Optional[str]
    dm_permission: Optional[bool] = True
    nsfw: Optional[bool] = False
    version: int
