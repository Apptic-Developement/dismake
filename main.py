import dismake, config
from dismake import SlashCommand, Option, Context
from dismake import Choice
from dismake.enums import OptionType


app = dismake.Bot(
    token=config.token,
    client_public_key=config.public_key,
    client_id=config.client_id,
    route="/",
)


@app.event("ready")
async def on_ready():
    print("Logged in as %s" % app.user)
    # await app.sync_commands()


class Autocomplete(SlashCommand):
    def __init__(self):
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
                    name='echo',
                    description="Echo something using autocomplete...",
                    type=OptionType.SUB_COMMAND,
                    options=[
                        Option(name='text', description="Type something...", required=True),
                        Option(name='type', description="Select a type for the echo...", required=True, autocomplete=True),
                    ]
                )
            ],
        )

    async def callback(self, ctx: Context):
        if ctx.subcommands.fruit:
            await ctx.respond(
                f"You got: {ctx.namespace.fav_fruit}\nQuantity: {ctx.namespace.quantity}\nThanks for shoping {ctx.namespace.name}!"
            )
        if ctx.subcommands.echo:
            await ctx.respond(
                f"**Type:** {ctx.namespace.type}\n\n{ctx.namespace.text}"
            )

    async def autocomplete(self, ctx: Context):
        if ctx.subcommands.fruit:
            focused = ctx.get_focused
            assert focused is not None
            if focused.name == "fav-fruit":
                fruits = ["Apple", "Banana", "Mango"]
                return [
                    Choice(name=fruit, value=fruit)
                    for fruit in fruits
                ]
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
            if focused.name == 'type':
                return [
                    Choice(name=echo) for echo in ech_type
                ]

class InfoCommand(SlashCommand):
    def __init__(self):
        super().__init__(name='info', description='Info about the dismake bot.')
    
    async def callback(self, ctx: Context):
        return await ctx.respond(
            f"""Hello! I'm a testing bot for the **dismake** library, a Python wrapper for the Discord Interaction API based on FastAPI. Our library is currently under development, but we're excited to bring you a powerful and user-friendly tool for creating interactive bots on Discord.

To answer your question, we're currently hosted on Vercel, a cloud platform that provides serverless functions and static sites. This allows us to easily deploy and scale our code, so we can focus on building great features for our users.

If you're interested in learning more about dismake or contributing to our project, check out our GitHub repository at <https://github.com/PranoyMajumdar/dismake>. We'd love to hear your feedback and ideas for making dismake even better.

Thanks for using our bot, and happy bot-making!

            """
        )
app.add_commands([Autocomplete(), InfoCommand()])


if __name__ == "__main__":
    app.run(app=f"main:app", reload=True)
