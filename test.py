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


from typing import Optional
from discord import ui
from discord.ext import commands
from config import token
import discord

import discord.state

class MyView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ui.Button(emoji="😂"))

bot = discord.Client(intents=discord.Intents.none())
@bot.event
async def on_ready():
    v = MyView()
    print(v.to_components())
bot.run(token)