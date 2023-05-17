from dismake import ui
import dismake
from dismake.models import Interaction
from dismake.models.interaction import Interaction
from dismake.ui import select

view = ui.View()


@view.string_select(
    options=[
        ui.SelectOption(label="Lund"),
        ui.SelectOption(label="Chut"),
        ui.SelectOption(label="Gand"),
    ]
)
async def select_callback(interaction: dismake.Interaction):
    await interaction.edit_message(f"You want {interaction.data.values[0]}")


@view.button(label="1")
async def b1(interaction: dismake.Interaction):
    await interaction.send("Hmm What ?", ephemeral=True)


@view.button(label="2")
async def b2(interaction: dismake.Interaction):
    await interaction.send("Hmm What ?", ephemeral=True)


# Modal


class MyModal(ui.Modal):
    def __init__(self) -> None:
        super().__init__("My modal")
        self.add_item(ui.TextInput("Name"))
        self.add_item(ui.TextInput("Age"))

    async def on_submit(self, interaction: Interaction):
        return await interaction.send(
            f"Name: {self.children[0].value}\nAge: {self.children[1].value}"
        )
