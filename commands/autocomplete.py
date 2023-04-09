from __future__ import annotations

from typing import TYPE_CHECKING
from dismake import SlashCommand, Context, Option, OptionType, Choice

if TYPE_CHECKING:
    from dismake import Bot


class Autocomplete(SlashCommand):
    def __init__(self, bot: Bot):
        super().__init__(
            name="autocomplete",
            description="Testing autocomplete.",
            options=[
                Option(
                    name="buy",
                    description="Buy products.",
                    type=OptionType.SUB_COMMAND_GROUP,
                    options=[
                        Option(
                            name="fruit",
                            description="Buy a fruit.",
                            type=OptionType.SUB_COMMAND,
                            options=[
                                Option(
                                    name="name", description="Your name?", required=True
                                ),
                                Option(
                                    name="fav-fruit",
                                    description="Fruits with your name.",
                                    autocomplete=True,
                                    required=True,
                                ),
                                Option(
                                    name="quantity",
                                    description="How many fruit(s) you want.",
                                    autocomplete=True,
                                    required=True,
                                ),
                            ],
                        )
                    ],
                ),
                Option(
                    name="echo",
                    description="Echo something using autocomplete...",
                    type=OptionType.SUB_COMMAND,
                    options=[
                        Option(
                            name="text", description="Type something...", required=True
                        ),
                        Option(
                            name="type",
                            description="Select a type for the echo...",
                            required=True,
                            autocomplete=True,
                        ),
                    ],
                ),
            ],
        )
        self.bot = bot

    async def callback(self, ctx: Context):
        if ctx.subcommands.fruit:
            await ctx.respond(
                f"You got: {ctx.namespace.fav_fruit}\nQuantity: {ctx.namespace.quantity}\nThanks for shoping {ctx.namespace.name}!"
            )
        if ctx.subcommands.echo:
            await ctx.respond(f"**Type:** {ctx.namespace.type}\n\n{ctx.namespace.text}")

    async def autocomplete(self, ctx: Context):
        if ctx.subcommands.fruit:
            focused = ctx.get_focused
            assert focused is not None
            if focused.name == "fav-fruit":
                fruits = ["Apple", "Banana", "Mango"]
                return [Choice(name=fruit, value=fruit) for fruit in fruits]
            elif focused.name == "quantity":
                quantitys = [
                    "One",
                    "Two",
                    "Three",
                ]
                return [Choice(name=name) for name in quantitys]
        elif ctx.subcommands.echo:
            ech_type = [
                f"Greetings",
                f"Coding",
                f"About You're self",
            ]
            focused = ctx.get_focused
            assert focused is not None
            if focused.name == "type":
                return [Choice(name=echo) for echo in ech_type]
