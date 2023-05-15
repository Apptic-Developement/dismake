from __future__ import annotations

from typing import Any, List, Optional, TYPE_CHECKING
from functools import wraps

from ..enums import ButtonStyles, ComponentType
from ..types import AsyncFunction
from .component import Component
from .button import Button
from .select import StringSelectMenu


if TYPE_CHECKING:
    from ..models import Interaction
    from .select import SelectOption
__all__ = ("View",)


class Row:
    """
    Represents an Action Row.
    """

    def __init__(self):
        self.components: List[Component] = list()

    @property
    def is_full(self) -> bool:
        if not self.components:
            return False
        if isinstance(self.components[0], (StringSelectMenu)):
            return len(self.components) == 1
        return len(self.components) == 5

    def add_component(self, component: Component):
        if self.is_full:
            raise ValueError("can't able to find free space to add the component.")
        self.components.append(component)
        return self

    def to_dict(self) -> dict[str, Any]:
        return {
            "type": ComponentType.ACTION_ROW.value,
            "components": [i.to_dict() for i in self.components],
        }


class View:
    """
    Represents a view that contains message components.

    Example
    --------
        view = View()
        @view.buttoon(label="Click me")
        async def click_me(ctx):
            await ctx.respond("Clicked")
    """

    def __init__(self) -> None:
        self.rows: List[Row] = list()
        self._error_handler: AsyncFunction = self.on_error

    @property
    def is_full(self) -> bool:
        return len(self.rows) == 5 and all(row.is_full for row in self.rows)

    async def on_error(self, interaction: Interaction, e: Exception) -> Any:
        pass

    def add_component(self, component: Component):
        if self.is_full:
            raise ValueError("can't able to find free space to add the component.")

        if isinstance(component, Button):
            if not self.rows or self.rows[-1].is_full:
                self.rows.append(Row())
            self.rows[-1].add_component(component)
        elif isinstance(component, (StringSelectMenu)):
            self.rows.append(Row().add_component(component))

    def button(
        self,
        label: Optional[str] = None,
        custom_id: Optional[str] = None,
        emoji: Optional[str] = None,
        style: Optional[ButtonStyles] = None,
        url: Optional[str] = None,
        disabled: Optional[bool] = None,
    ):
        def decorator(coro: AsyncFunction):
            @wraps(coro)
            def wrapper(*_, **__):
                button = Button(
                    label=label,
                    custom_id=custom_id,
                    style=style,
                    url=url,
                    disabled=disabled,
                    emoji=emoji,
                )
                button.callback = coro
                self.add_component(button)
                return button

            return wrapper()

        return decorator

    def string_select(
        self,
        options: List[SelectOption],
        placeholder: Optional[str] = None,
        custom_id: Optional[str] = None,
        min_values: int = 1,
        max_values: int = 1,
        disabled: bool = False,
    ):
        def decorator(coro: AsyncFunction):
            @wraps(coro)
            def wrapper(*_, **__):
                select = StringSelectMenu(
                    placeholder=placeholder,
                    options=options,
                    custom_id=custom_id,
                    min_values=min_values,
                    max_values=max_values,
                    disabled=disabled,
                )
                select.callback = coro
                self.add_component(select)
                return select

            return wrapper()

        return decorator

    def add_url_button(
        self, label: str, url: str, emoji: str, disabled: Optional[bool]
    ):
        button = Button(
            label=label,
            url=url,
            style=ButtonStyles.link,
            emoji=emoji,
            disabled=disabled,
            custom_id=None,
        )
        self.add_component(button)
        return button

    def error(self, coro: AsyncFunction):
        @wraps(coro)
        def wrapper(*_, **__):
            self._error_handler = coro
            return coro

        return wrapper()

    def to_dict(self) -> list[dict[str, Any]]:
        return [row.to_dict() for row in self.rows]
