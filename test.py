from dismake import app_commands

command_1 = app_commands.Group(name="slash", description="This is main command.")
command_2 = app_commands.Group(
    name="slash_group", description="This is slash group command.", parent=command_1
)


@command_1.command("sub_command1", "This is a sub command")
async def sub_command_c1_1():
    ...


@command_1.command("sub_command2", "This is a sub command")
async def sub_command_c1_2():
    ...


@command_2.command("sub_command3", "This is a sub command")
async def sub_command_c2_1():
    ...


@command_2.command("sub_command4", "This is a sub command")
async def sub_command_c2_2():
    ...


print(command_1.to_dict())
