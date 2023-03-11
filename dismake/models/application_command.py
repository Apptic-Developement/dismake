from pydantic import BaseModel
from typing import Optional, List, Dict, Union



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
    name_localizations: Optional[Dict[str, str]]
    description: Optional[str] = "No description provided"
    description_localizations: Optional[Dict[str, str]]
    required: Optional[bool] = False
    choices: Optional[List[ApplicationCommandChoice]]
    options: Optional[List["ApplicationCommandOption"]]
    channel_types: Optional[List[str]]
    min_value: Optional[Union[int, float]]
    max_value: Optional[Union[int, float]]
    min_length: Optional[int]
    max_length: Optional[int]
    autocomplete: Optional[bool]


class ApplicationCommand(BaseModel):
    id: int
    type: int = 1
    application_id: int
    guild_id: Optional[int]
    name: str
    name_localizations: Optional[Dict[str, str]]
    description: Optional[str] = "No description provided"
    description_localizations: Optional[Dict[str, str]]
    options: Optional[List[ApplicationCommandOption]]
    default_member_permissions: Optional[str]
    dm_permission: Optional[bool] = True
    default_permission: Optional[bool] = True
    nsfw: Optional[bool] = False
    version: int