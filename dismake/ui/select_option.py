from __future__ import annotations
from typing import Any, Optional

from pydantic import BaseModel 

__all__ = (
    "SelectOption",
)

class SelectOption(BaseModel):
    label: str
    value: str
    description: Optional[str]
    emoji: Optional[Any]
    default: Optional[bool]
    