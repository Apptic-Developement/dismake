from __future__ import annotations
import uuid
from typing import Any, Dict, List, Optional
from ..enums import ButtonStyles, ComponentTypes
from ..types import AsyncFunction
from pydantic import BaseModel
from functools import wraps

__all__ = ("Component",)


class Component:
    def __init__(self, type: ComponentTypes) -> None:
        self.type = type
        self._callback: Optional[AsyncFunction] = None

    @property
    def callback(self) -> AsyncFunction:
        assert self._callback is not None
        return self._callback

    def to_dict(self) -> Dict[str, Any]:
        base = {"type": self.type.value}
        return base
