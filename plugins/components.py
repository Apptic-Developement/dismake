from dismake import app_commands, ui, Plugin
import dismake
from test import view

plugin = Plugin()


components = plugin.create_group(
    name="components",
    description="This group holds all the components related commands.",
)


@components.command(name="button_and_select", description="...")
async def button_command(interaction: dismake.Interaction):
    await interaction.respond("Ok", view=view)
