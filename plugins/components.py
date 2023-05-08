from dismake import app_commands, ui, Plugin
import dismake

house = ui.House()


@house.button(emoji="<:prishu_juicepeetihui:928222783069093888>")
async def bcb(interaction: dismake.Interaction):
    await interaction.send(f"Ok? {interaction.user}")


@house.button(emoji="👀")
async def bcb2(interaction: dismake.Interaction):
    await interaction.send(f"Ok? {interaction.user}")


plugin = Plugin()


components = plugin.create_group(
    name="components",
    description="This group holds all the components related commands.",
)


@components.command(
    name="button", description="A button which says 'Hii' to the invoker."
)
async def button_command(interaction: dismake.Interaction):
    await interaction.send("Ok", house=house)
