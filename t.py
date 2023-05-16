from typing import Annotated
from dismake import ui, Interaction

modal = ui.Modal(title="Okiee?")


@modal.on_submit
async def callback(
    interaction: Interaction,
    o1: Annotated[str, ui.TextInput()],
    o2: Annotated[str, ui.TextInput()],
    o3: Annotated[str, ui.TextInput()],
    o4: Annotated[str, ui.TextInput()],
    o5: Annotated[str, ui.TextInput()],
):
    ...


print(modal.to_dict())
