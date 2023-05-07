import dismake
from dismake import app_commands
from typing import Annotated


plugin = dismake.Plugin()

mentions = plugin.create_group(
    name="mentions", description="This group holds only mentions commands."
)

@mentions.command(name="echo", description="Echo command.")
async def echo_command(
    interaction,
    text: Annotated[
        str,
        app_commands.Option(),
    ],
):
    await interaction.send(f"{text}")


@mentions.command(name="user", description="User mention command.")
async def user_command(
    interaction,
    user: Annotated[
        dismake.User,
        app_commands.Option(),
    ],
):
    await interaction.send(f"Mentioned: {user.mention}")


@mentions.command(name="role", description="Role mention command.")
async def role_command(
    interaction,
    role1: Annotated[
        dismake.Role,
        app_commands.Option(),
    ],
    role2: Annotated[
        dismake.Role,
        app_commands.Option(),
    ],
    role3: Annotated[
        dismake.Role,
        app_commands.Option(),
    ],
):
    await interaction.send(
        f"Mentioned -\n>>> \nRole 1: {role1.mention}\nRole 2: {role2.mention}\nRole 3: {role3.mention}"
    )



@mentions.command(name="autocomplete", description="This sub command is have a autocomplete option.")
async def autocomplete(interaction: dismake.Interaction,
    fav_fruit: Annotated[str, app_commands.Option(autocomplete=True)],
    fav_fruit2: Annotated[str, app_commands.Option(autocomplete=True)],
    fav_fruit3: Annotated[str, app_commands.Option(autocomplete=True)],
    ):
    await interaction.send(f"Ok {fav_fruit}")