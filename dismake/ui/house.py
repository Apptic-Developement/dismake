from __future__ import annotations

from typing import Any, Dict, List, Optional
from functools import wraps

from ..enums import ButtonStyles, ComponentTypes
from ..types import AsyncFunction
from .component import Component
from .button import Button
from ..errors import ComponentException
from ..utils import chunk
__all__ = ("House",)


class House:
    def __init__(self) -> None:
        self.components: List[Component] = []

    def add_component(self, component: Component):
        if len(self.components) == 25:
            raise ComponentException(
                "You can not add more than 25 components."
            )
        exists = list(
            filter(lambda x: x.custom_id == component.custom_id, self.components)
        )
        if exists:
            return
        self.components.append(component)

    def button(
        self,
        label: str,
        custom_id: Optional[str] = None,
        style: Optional[ButtonStyles] = None,
        url: Optional[str] = None,
        disabled: Optional[bool] = None
    ):
        def decorator(coro: AsyncFunction):
            @wraps(coro)
            def wrapper(*_, **__):
                button = Button(label=label, custom_id=custom_id, style=style, url=url, disabled=disabled)
                button.callback = coro
                self.add_component(button)
                return button

            return wrapper()

        return decorator

    def to_dict(self) -> List[Dict[str, Any]]:
        comps: List[List[Component]] = list()
        for items in chunk(5, self.components):
            comps.append([item.to_dict() for item in items])

        return [
            {
                "type": ComponentTypes.ACTION_ROW.value,
                "components": [five for five in comp],
            } for comp in comps
        ]