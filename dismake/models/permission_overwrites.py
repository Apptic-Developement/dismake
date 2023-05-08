from __future__ import annotations
from typing import Literal
from pydantic import BaseModel
from ..permissions import Permissions
from ..types import SnowFlake
__all__ = (
    "PermissionOverwrites",
)
class PermissionOverwrites(BaseModel):
    id: SnowFlake
    type: Literal[0, 1]
    allow: Permissions
    deny: Permissions