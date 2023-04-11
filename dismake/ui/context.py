from __future__ import annotations
from typing import List, Optional

from ..interaction import Interaction
from .select_option import SelectOption
from pydantic import BaseModel
from ..enums import InteractionType
__all__ = ("ComponentContext", "ModalContext")


class MessageComponentData(BaseModel):
    custom_id: str
    component_type: int
    values: Optional[List[SelectOption]]


class ModalSubmitData(BaseModel):
    custom_id: str
    # components	array of message components	the values submitted by the user

class ComponentContext(Interaction):
    data: Optional[MessageComponentData]



class ModalContext(Interaction):
    data: Optional[ModalSubmitData]
