from dismake import app_commands, ui, Plugin
import dismake


plugin = Plugin()


components = plugin.create_group(
    name="components",
    description="This group holds all the components related commands.",
)


@components.command(name="button_select", description="...")
async def button_command(interaction: dismake.Interaction):
    res = await interaction.respond("Ok")
    print(res.json())
