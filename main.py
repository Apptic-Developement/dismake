import dismake, config
from dismake.interaction import Interaction

app = dismake.Bot(
    token=config.token, client_public_key=config.public_key, client_id=config.client_id
)

@app.on_event("startup")
async def on_startup():
    # print(await app.sync_commands())
    pass


@app.command(name="alive", description="alive ?")
async def alive(interaction: Interaction):
    await interaction.respond("Yes im alive :), Thanks to Pranoy & Dismake Daddy.")

if __name__ == "__main__":
    app.run(app=f"main:app", reload=True)

