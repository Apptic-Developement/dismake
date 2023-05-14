from __future__ import annotations
import uuid
from typing import Any, Dict, Optional, TYPE_CHECKING
from ..enums import ComponentType

if TYPE_CHECKING:
    from .view import View
    from ..models import Interaction

__all__ = ("Component",)


class Component:
    def __init__(
        self, type: ComponentType, custom_id: Optional[str], disabled: Optional[bool]
    ) -> None:
        self.type = type
        self.custom_id = custom_id or str(uuid.uuid4())
        self.disabled = disabled
        self._view: View

    @property
    def view(self) -> View:
        return self._view

    @view.setter
    def view(self, v: View) -> View:
        self.view = v
        return self.view

    async def callback(self, interaction: Interaction) -> Any:
        ...

    def to_dict(self) -> Dict[str, Any]:
        base = {"type": self.type.value, "custom_id": self.custom_id}
        if self.disabled:
            base["disabled"] = self.disabled
        return base
