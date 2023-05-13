import dismake, config
from plugins import mentions, components, autocomplete


app = dismake.Bot(
    token=config.token,
    client_public_key=config.public_key,
    client_id=config.client_id,
    route="/",
)


mentions.plugin.load(app)
components.plugin.load(app)
autocomplete.plugin.load(app)


@app.event()
async def on_ready():
    app.log.info("Logged in as %s" % app.user)
    # sync = await app.sync_commands()
    # print(sync.text)


if __name__ == "__main__":
    app.run(app=f"main:app", reload=True)
