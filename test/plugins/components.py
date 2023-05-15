from dismake import ui, Plugin
import dismake
from tests import view

plugin = Plugin()


components = plugin.create_group(
    name="components",
    description="This group holds all the components related commands.",
)


@components.command(name="button_and_select", description="...")
async def button_command(interaction: dismake.Interaction):
    await interaction.respond("Ok", view=view)


@components.command()
async def modal(interaction: dismake.Interaction):
    modal = ui.Modal(title="My Special Modal")
    modal.add_item(ui.TextInput(label="Your name"))
    res = await interaction.respond_with_modal(modal)
    print(res)