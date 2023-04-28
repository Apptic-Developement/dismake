import dismake, config, logging
from commands import get_commands

log = logging.getLogger(__name__)
app = dismake.Bot(
    token=config.token,
    client_public_key=config.public_key,
    client_id=config.client_id,
    route="/",
)


@app.event("ready")
async def on_ready():
    log.info("Logged in as %s" % app.user)
    await app.sync_commands()


# @app.event(dismake.Events.InteractionCreate)
# async def interaction_create(interaction: dismake.Interaction, payload: dict):
#     print(payload)


app.add_commands(get_commands(app))


if __name__ == "__main__":
    app.run(app=f"main:app", reload=True)
