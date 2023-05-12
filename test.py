# import typing as t
# import inspect
# from dismake import app_commands
# from dismake.app_commands.commands import Option


# def command(
#     name: t.Annotated[str, app_commands.Option(max_value=1, min_value=2)],
#     age: t.Annotated[
#         int,
#         app_commands.Option(
#             name="age", description="This is age field", max_value=1, min_value=2
#         ),
#     ] = 1,
#     optional: str = "Hmm",
# ):
#     ...


# def validate_options(func: t.Callable):
#     params = inspect.signature(command).parameters
#     options: list[Option] = list()
#     for k, v in params.items():
#         """
#         k: The name of the function
#             - name
#         v: The annotation of the function
#             - typing.Annotated[str, <Option name="foo">]
#         """
#         annotation = v.annotation
#         if t.get_origin(annotation) != t.Annotated:
#             continue
#         option_type: type = annotation.__args__[0]
#         option_object: Option = annotation.__metadata__[0]
#         option_object.type = app_commands.commands._option_types[option_type]
#         if option_object.description is None and (doc := func.__doc__) is not None:
#             option_object.description = inspect.cleandoc(doc)
#         if option_object.description is None and func.__doc__ is None:
#             option_object.description = "..."

#         if option_object.name is None:
#             option_object.name = k

#         if option_object.required is None:
#             if v.default != inspect._empty:
#                 option_object.required = False
#             else:
#                 option_object.required = True

#         options.append(option_object)


# validate_options(command)


# type: ignore
# from typing import Dict, List, Union

# def extract_options(option: ApplicationCommandOption) -> List[ApplicationCommandOption]:
#     """Recursively extract options from sub-command groups"""
#     if option.type == OptionType.SUB_COMMAND.value and option.options is not None:
#         return [o for sub_opt in option.options for o in extract_options(sub_opt)]
#     elif option.type == OptionType.SUB_COMMAND_GROUP.value and option.options is not None:
#         return [o for sub_group in option.options for o in extract_options(sub_group)]
#     else:
#         return [option]

# def options_to_dict(options: List[ApplicationCommandOption], resolved_data: ApplicationCommandInteractionDataResolved) -> Dict[str, Union[str, None]]:
#     """Convert options to a dictionary"""
#     namespace_dict = {}
#     for option in options:
#         if option.type == OptionType.USER.value:
#             if resolved_data is not None and resolved_data.users is not None:
#                 user_id = str(option.value)
#                 namespace_dict[option.name.replace("-", "_")] = resolved_data.users.get(user_id)
#         elif option.type == OptionType.ROLE.value:
#             if resolved_data is not None and resolved_data.roles is not None:
#                 role_id = str(option.value)
#                 namespace_dict[option.name.replace("-", "_")] = resolved_data.roles.get(role_id)
#         else:
#             namespace_dict[option.name.replace("-", "_")] = option.value if not isinstance(option, ApplicationCommandGroup) else None
#     return namespace_dict

# @property
# def namespace(self) -> Dict[str, Union[str, None]]:
#     """Extract options from interaction payload and return them as a dictionary"""
#     if not isinstance(self.data, ApplicationCommandData):
#         return {}
#     data = self.data
#     if data.options is None:
#         return {}
#     resolved_data = data.resolved
#     options = [o for option in data.options for o in extract_options(option)]
#     if not options:
#         return {}

#     return options_to_dict(options, resolved_data)

# import dismake, typing as t, inspect
# def command(channel: t.Union[dismake.TextChannel, dismake.CategoryChannel]):
#     ...

# def get_union_values(func: t.Callable):
#     params = inspect.signature(func).parameters
#     for k, v in params.items():
#         print(t.get_args(v.annotation))

# get_union_values(command)


# import discord
# from config import token
# from discord.ext import commands
# from discord import ui


# class MyView(ui.View):
#     def __init__(self):
#         super().__init__(timeout=120)
#         self.add_item

#     @ui.button(label="Button 1")
#     async def b1cb(self, *_, **__):
#         ...

#     @ui.button(label="Button 2")
#     async def b2cb(self, *_, **__):
#         ...

#     # @ui.button(label="Button 3")
#     # async def b3cb(self, *_, **__):
#     #     ...

#     # @ui.button(label="Button 4")
#     # async def b4cb(self, *_, **__):
#     #     ...

#     # @ui.button(label="Button 5")
#     # async def b5cb(self, *_, **__):
#     #     ...

#     @ui.select()
#     async def select1cb(self, *_, **__):
#         ...

#     @ui.select()
#     async def select2cb(self, *_, **__):
#         ...

#         # @ui.select()
#         # async def select3cb(self, *_, **__):
#         #     ...

#         # @ui.select()
#         # async def select4cb(self, *_, **__):
#         #     ...

#         # @ui.select()
#         # async def select5cb(self, *_, **__):
#         ...


# bot = commands.Bot(command_prefix="1", intents=discord.Intents.none())


# @bot.event
# async def on_ready():
#     print(MyView().to_components())


# bot.run(token)

from dismake import ui
from pprint import pprint
import dismake

view = ui.View()

@view.string_select(options=[
    ui.SelectOption(label="Lund"),
    ui.SelectOption(label="Chut"),
    ui.SelectOption(label="Gand"),
])
async def select_callback(interaction: dismake.Interaction):
    await interaction.edit_message(f"You want {interaction.data.values[0]}")

@view.button(label="1")
async def b1(interaction: dismake.Interaction):
    await interaction.send("Hmm What ?", ephemeral=True)


@view.button(label="2")
async def b2(interaction: dismake.Interaction):
    await interaction.send("Hmm What ?", ephemeral=True)


