import dismake
import typing as t
from dismake import app_commands


plugin = dismake.Plugin()


ag = plugin.create_group(
    name="autocomplete", description="This group holds all the autocomplete commands."
)


@plugin.command(name="sub_command", description="This is an autocomplete sub command.")
async def command(
    interaction: dismake.Interaction,
    fruit1: t.Annotated[str, app_commands.Option(autocomplete=True)],
    fruit2: t.Annotated[str, app_commands.Option(autocomplete=True)],
    fruit3: t.Annotated[str, app_commands.Option(autocomplete=True)],
):
    await interaction.send(f"Fruit 1: {fruit1}\nFruit 2: {fruit2}\nFruit 3: {fruit3}")


@ag.command(name="sub_command", description="This is an autocomplete sub command.")
async def sub_command(
    interaction: dismake.Interaction,
    fruit1: t.Annotated[str, app_commands.Option(autocomplete=True)],
    fruit2: t.Annotated[str, app_commands.Option(autocomplete=True)],
    fruit3: t.Annotated[str, app_commands.Option(autocomplete=True)],
):
    await interaction.send(f"Fruit 1: {fruit1}\nFruit 2: {fruit2}\nFruit 3: {fruit3}")


sub_group = ag.create_sub_group(
    name="sub_group",
    description="This sub group also holds some autocomplete commands.",
)


@sub_group.command(
    name="sub_group_command", description="This is also an sub group command."
)
async def sub_group_command(
    interaction: dismake.Interaction,
    fruit1: t.Annotated[str, app_commands.Option(autocomplete=True)],
    fruit2: t.Annotated[str, app_commands.Option(autocomplete=True)],
    fruit3: t.Annotated[str, app_commands.Option(autocomplete=True)],
):
    await interaction.send(f"Fruit 1: {fruit1}\nFruit 2: {fruit2}\nFruit 3: {fruit3}")


@sub_command.autocomplete("fruit1")
@sub_command.autocomplete("fruit2")
@sub_command.autocomplete("fruit3")
@sub_group_command.autocomplete("fruit1")
@sub_group_command.autocomplete("fruit2")
@sub_group_command.autocomplete("fruit3")
@command.autocomplete("fruit1")
@command.autocomplete("fruit2")
@command.autocomplete("fruit3")
async def autocomplete_callback(interaction: dismake.Interaction):
    fruits = ["Mango", "Apple", "Banana", "Pineaple", "Graps", "Strawberry", "Berry"]
    return [app_commands.Choice(name=fruit) for fruit in fruits]
