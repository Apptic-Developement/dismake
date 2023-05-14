import dismake
from typing import Annotated


plugin = dismake.Plugin(__name__)

mentions = plugin.create_group(
    name="mentions", description="This group holds only mentions dismake."
)

channels = plugin.create_group(
    name="channels", description="This group holds only channels dismake."
)


@plugin.on_load
async def on_load():
    plugin.bot.log.info(f"{plugin.name!r} loaded successfully.")


@mentions.command(name="echo", description="Echo command.")
async def echo_command(
    interaction,
    text: Annotated[
        str,
        dismake.Option(),
    ],
):
    await interaction.send(f"{text}")


@mentions.command(name="user", description="User mention command.")
async def user_command(
    interaction,
    user: Annotated[
        dismake.User,
        dismake.Option(),
    ],
):
    await interaction.send(f"Mentioned: {user.mention}")


@mentions.command(name="role", description="Role mention command.")
async def role_command(
    interaction,
    role1: Annotated[
        dismake.Role,
        dismake.Option(),
    ],
    role2: Annotated[
        dismake.Role,
        dismake.Option(),
    ],
    role3: Annotated[
        dismake.Role,
        dismake.Option(),
    ],
):
    await interaction.send(
        f"Mentioned -\n>>> \nRole 1: {role1.mention}\nRole 2: {role2.mention}\nRole 3: {role3.mention}"
    )


@channels.command(name="text", description="This channel mentions a text channel.")
async def text_mention(
    interaction: dismake.Interaction,
    channel: Annotated[dismake.TextChannel, dismake.Option()],
):
    await interaction.send(f"Mentioned: {channel.mention}")


@channels.command(
    name="category", description="This channel mentions a category channel."
)
async def category_mention(
    interaction: dismake.Interaction,
    channel: Annotated[
        dismake.CategoryChannel,
        dismake.Option(channel_types=[dismake.ChannelType.GUILD_CATEGORY]),
    ],
):
    await interaction.send(f"Mentioned: {channel.mention}")
