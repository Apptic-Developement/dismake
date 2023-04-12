from dismake import SlashCommand, Context, Bot, Option, OptionType
from test import house
class Component(SlashCommand):
    def __init__(self, bot: Bot):
        super().__init__(
            name="components",
            description="Testing components.",
            options=[
                Option(
                    name="button",
                    description="Test button.",
                    type=OptionType.SUB_COMMAND,
                )
            ],
        )

    async def callback(self, ctx: Context):
        if ctx.namespace.button:
            await ctx.respond(f"Button", houses=[house])

