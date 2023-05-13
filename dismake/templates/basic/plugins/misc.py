import dismake
import typing

__all__ = ("plugin",)
plugin = dismake.Plugin()


@plugin.command(name="echo", description="A simple echo command")
async def echo_command(
    interaction: dismake.Interaction, text: typing.Annotated[str, dismake.Option()]
):
    """A simple echo command which takes an argument called `text` and send a respond with that argument."""
    await interaction.respond(text)
