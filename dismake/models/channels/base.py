from __future__ import annotations

from pydantic import BaseModel
from ...types import SnowFlake


class Channel(BaseModel):
    id: SnowFlake
    type: int