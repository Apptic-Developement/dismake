from __future__ import annotations
import uuid
from typing import Any, Dict, Optional, TYPE_CHECKING

from dismake.types import AsyncFunction
from ..enums import ComponentType

if TYPE_CHECKING:
    from .view import View
    from ..models import Interaction

__all__ = ("Component",)


class Component:
    """
    Represents a Discord component.

    This class should not be initialized directly.
    All other components should subclass this class.

    Parameters
    ----------
    type: :class:`ComponentType`
        The type of the component.
    custom_id: :class:`str`
        The custom ID of the component. If not provided, a random UUID will be generated.
    disabled: :str:`bool`
        Indicates whether the component is disabled.

    Attributes
    ----------
    view: :class:`View`
        The view associated with the component.
    """

    def __init__(
        self, type: ComponentType, custom_id: Optional[str], disabled: Optional[bool]
    ) -> None:
        self.type = type
        self.custom_id = custom_id or str(uuid.uuid4())
        self.disabled = disabled
        self._view: View
        self._callback: AsyncFunction | None = None

    @property
    def view(self) -> View:
        """
        Returns the view associated with the component.
        """
        return self._view

    @view.setter
    def view(self, v: View) -> View:
        self.view = v
        return self.view


    def to_dict(self) -> Dict[str, Any]:
        """
        Converts a component into a dict.

        Returns
        -------
        dict[str, Any]
        """
        base = {"type": self.type.value, "custom_id": self.custom_id}
        if self.disabled:
            base["disabled"] = self.disabled
        return base
