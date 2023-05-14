import dismake, config
from plugins import mentions, components, autocomplete

# mypy --show-error-codes --pretty dismake

app = dismake.Bot(
    token=config.token,
    client_public_key=config.public_key,
    client_id=config.client_id,
    route="/",
)


@app.event()
async def on_ready():
    app.log.info("Logged in as %s" % app.user)
    await mentions.plugin.load(app)
    await components.plugin.load(app)
    await autocomplete.plugin.load(app)
    # sync = await app.sync_commands()
    # print(sync.text)


if __name__ == "__main__":
    app.run(app=f"main:app", reload=True)
