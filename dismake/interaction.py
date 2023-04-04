from __future__ import annotations

from typing import Any, Optional, TYPE_CHECKING, List, Union
from pydantic import BaseModel
from .enums import InteractionType
from .types import SnowFlake
from .models import Member, User

if TYPE_CHECKING:
    from .client import Bot

__all__ = ("Interaction",)


class InteractionSlashOption(BaseModel):
    name: str
    type: int
    value: Optional[Union[str, int, float, bool]]
    options: List[InteractionSlashOption]
    focused: bool = False


class InteractionData(BaseModel):
    id: SnowFlake
    name: str
    type: int
    resolved: Optional[Any]
    options: Optional[List[InteractionSlashOption]]
    guild_id: Optional[SnowFlake]
    target_id: Optional[SnowFlake]
    custom_id: str
    component_type: int
    values: List[
        Any
    ]  # array of select option values	values the user selected in a select menu component
    components: List[
        Any
    ]  # 	array of message components	the values submitted by the user

class InteractionOption:
    def __init__(self):
        ...
    
class Interaction(BaseModel):
    client: Bot

    id: SnowFlake
    application_id: SnowFlake
    type: int
    data: Optional[InteractionData]
    guild_id: Optional[SnowFlake]
    channel_id: Optional[SnowFlake]
    member: Optional[Member]
    user: Optional[User]
    token: str
    version: int
    message: Optional[Any]
    app_permissions: Any
    locale: Any
    guild_locale: Any


    
