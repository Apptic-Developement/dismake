from __future__ import annotations
import uuid
from typing import Any, Dict, Optional, TYPE_CHECKING
from ..enums import ComponentTypes

if TYPE_CHECKING:
    from .house import House
    from .context import ComponentContext

__all__ = ("Component",)


class Component:
    def __init__(
        self, type: ComponentTypes, custom_id: Optional[str], disabled: Optional[bool]
    ) -> None:
        self.type = type
        self.custom_id = custom_id or str(uuid.uuid4())
        self.disabled = disabled
        self._house: House

    @property
    def house(self) -> House:
        return self._house

    @house.setter
    def house(self, h: House) -> House:
        self._house = h
        return self._house

    async def callback(self, ctx: ComponentContext) -> Any:
        ...

    def to_dict(self) -> Dict[str, Any]:
        base = {"type": self.type.value, "custom_id": self.custom_id}
        if self.disabled:
            base["disabled"] = self.disabled
        return base
