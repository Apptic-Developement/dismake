import dismake, config
from dismake.enums import OptionType
from dismake.interaction import Interaction

app = dismake.Bot(
    token=config.token, client_public_key=config.public_key, client_id=config.client_id
)


@app.on_event("startup")
async def on_startup():
    # print(await app.sync_commands())
    pass


code = """
@app.command(name="echo", description="Echo", options=[
    dismake.Option(name='text', description="Say something.", required=True),
    dismake.Option(name='show_code', description="If this option is choosed then i will show you the code of this command.", required=True, type=OptionType.BOOLEAN),
])
async def alive(interaction: Interaction):
    if interaction.data.options[1].value == "False":
        await interaction.respond(f"**You Said**: \n{interaction.data.options[0].value}")
    else:
        pass # Skipped for some pertional reason.

"""


@app.command(
    name="echo",
    description="Echo",
    options=[
        dismake.Option(name="text", description="Say something.", required=True),
        dismake.Option(
            name="show_code",
            description="If this option is choosed then i will show you the code of this command.",
            required=True,
            type=OptionType.BOOLEAN,
        ),
    ],
)
async def alive(interaction: Interaction):
    if interaction.data.options[1].value == "False":
        await interaction.respond(
            f"**You Said**: \n{interaction.data.options[0].value}"
        )
    else:
        await interaction.respond(
            f"**You Said**: \n{interaction.data.options[0].value}\n\n**Code**: \n```py\n{code}\n```"
        )


if __name__ == "__main__":
    app.run(app=f"main:app", reload=True)
