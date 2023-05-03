# from dismake import app_commands

# command_1 = app_commands.Group(name="slash", description="This is main command.")
# command_2 = app_commands.Group(
#     name="slash_group", description="This is slash group command.", parent=command_1
# )


# @command_1.command("sub_command1", "This is a sub command")
# async def sub_command_c1_1():
#     ...


# @command_1.command("sub_command2", "This is a sub command")
# async def sub_command_c1_2():
#     ...


# @command_2.command("sub_command3", "This is a sub command")
# async def sub_command_c2_1():
#     ...


# @command_2.command("sub_command4", "This is a sub command")
# async def sub_command_c2_2():
#     ...


# print(command_1.to_dict())
# import inspect, dismake
# from dismake import app_commands
# from typing import Annotated, get_origin


# group = app_commands.Group(name="slash", description="This is main command.")
# sub_group = group.create_sub_group(
#     name="sub_group", description="This is sub group command."
# )

# @group.command("sub_command1", "This is a sub command 1.")
# async def sub_command1(ctx, name: Annotated[str, app_commands.Option("name", "What is your name?")]):
    
#     await ctx.send(f"Your name is: {name} ?")

# print(group.to_dict())

from discord.interactions import Interaction 
Interaction