from __future__ import annotations
import uuid
from typing import Any, Dict, Optional, TYPE_CHECKING
from ..enums import ComponentTypes
if TYPE_CHECKING:
    from .context import ComponentContext

__all__ = ("Component",)


class Component:
    def __init__(self, type: ComponentTypes, custom_id: Optional[str], disabled: Optional[bool]) -> None:
        self.type = type
        self.custom_id = custom_id or str(uuid.uuid4())
        self.disabled = disabled

    async def callback(self, ctx: ComponentContext) -> Any:
        ...

    def to_dict(self) -> Dict[str, Any]:
        base = {"type": self.type.value, "custom_id": self.custom_id}
        if self.disabled:
            base['disabled'] = self.disabled
        return base
