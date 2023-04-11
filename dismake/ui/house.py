from __future__ import annotations

from typing import Any, Dict, List, Optional
from functools import wraps

from ..enums import ButtonStyles, ComponentTypes
from ..types import AsyncFunction
from .component import Component
from .button import Button
from ..errors import HouseError

__all__ = ("House",)


class House:
    def __init__(self) -> None:
        self._components: List[Component] = []

    def add_component(self, component: Component):
        if len(self._components) == 5:
            raise HouseError("A house can only have 5 components.")
        exists = list(
            filter(lambda x: x.custom_id == component.custom_id, self._components)
        )
        if exists:
            return
        self._components.append(component)

    def button(
        self,
        label: str,
        custom_id: Optional[str] = None,
        style: Optional[ButtonStyles] = None,
        url: Optional[str] = None,
    ):
        def decorator(coro: AsyncFunction):
            @wraps(coro)
            def wrapper(*_, **__):
                button = Button(label=label, custom_id=custom_id, style=style, url=url)
                button._callback = coro
                self.add_component(button)

            return wrapper()

        return decorator

    def to_dict(self) -> Dict[str, Any]:
        base = {
            "type": ComponentTypes.ACTION_ROW.value,
            "components": [component.to_dict() for component in self._components],
        }
        return base
