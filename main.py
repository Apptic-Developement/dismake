import dismake, config
from commands import get_commands

app = dismake.Bot(
    token=config.token,
    client_public_key=config.public_key,
    client_id=config.client_id,
    route="/",
)


@app.event(dismake.Events.Ready)
async def on_ready():
    print("Logged in as %s" % app.user)
    # await app.sync_commands()


@app.event(dismake.Events.InteractionCreate)
async def interaction_create(interaction: dismake.Interaction, payload: dict):
    print(interaction.bot.user)


app.add_commands(get_commands(app))


if __name__ == "__main__":
    app.run(app=f"main:app", reload=True)
