import dismake
from dismake import app_commands
from typing import Annotated

tree = dismake.CommandTree()

mentions = tree.create_group(
    name="mentions", description="This group holds only mentions commands."
)
# channels = mentions.create_sub_group(
#     name="channels", description="This sub group holds only channel mention commands."
# )

components = mentions.create_sub_group(
    name="components",
    description="This sub group holds all the components related commands.",
)


@mentions.command(name="echo", description="Echo command.")
async def echo_command(
    ctx,
    text: Annotated[
        str,
        app_commands.Option(
            name="echo",
            description="Type something...",
            required=True,
            type=str,
        ),
    ],
):
    await ctx.send(f"{text}")


@mentions.command(name="user", description="User mention command.")
async def user_command(
    ctx,
    user: Annotated[
        dismake.User,
        app_commands.Option(
            name="user",
            description="Select a user...",
            required=True,
            type=dismake.OptionType.USER,
        ),
    ],
):
    await ctx.send(f"Mentioned: {user.mention}")


@mentions.command(name="role", description="Role mention command.")
async def role_command(
    ctx,
    role1: Annotated[
        dismake.Role,
        app_commands.Option(
            name="role",
            description="Select a role...",
            required=True,
            type=dismake.Role,
        ),
    ],
    role2: Annotated[
        dismake.Role,
        app_commands.Option(
            name="role2",
            description="Select a role...",
            required=True,
            type=dismake.Role,
        ),
    ],
    role3: Annotated[
        dismake.Role,
        app_commands.Option(
            name="role3",
            description="Select a role...",
            required=True,
            type=dismake.Role,
        ),
    ],
):
    await ctx.send(
        f"Mentioned -\n>>> \nRole 1: {role1.mention}\nRole 2: {role2.mention}\nRole 3: {role3.mention}"
    )


@components.command(
    name="button", description="A button which says 'Hii' to the invoker."
)
async def button_command(ctx):
    # TODO
    pass
