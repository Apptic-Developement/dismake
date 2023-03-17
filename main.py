import dismake, config
from dismake.interaction import Interaction

app = dismake.Bot(
    token=config.token, client_public_key=config.public_key, client_id=config.client_id
)

@app.on_event("startup")
async def on_startup():
    # print(await app.sync_commands())
    pass


@app.command(name="rolemenu", description="Rolemenu command")
async def rolemenu(interaction): pass


@rolemenu.sub_command(name="create", description="Okiee?")
async def rc(interaction): pass

@rc.sub_command(name='something', description="Hmmm")
async def rcs(interaction: Interaction):
    await interaction.respond("Called.")

@rolemenu.sub_command(name="delete", description="Delete okiee??", options=[
    dismake.Option(name="cname", description="cname", required=True),
    dismake.Option(name="buttons", description="buttons", required=True, choices=[
        dismake.Choice(name='B1'),
        dismake.Choice(name='B2'),
        dismake.Choice(name='B3'),
        dismake.Choice(name='B4'),
    ]),
])
async def rd(interaction: Interaction):
    await interaction.respond("delete")

@app.command(
    name="ban",
    description="Ban a randi"
)
async def ban(interaction: Interaction):
    await interaction.respond("ban")
if __name__ == "__main__":
    app.run(app=f"main:app", reload=True)

