from typing import Union
import dismake, config
from plugins import autocomplete, mentions, components


# mypy --show-error-codes --pretty --check-untyped-defs dismake

app = dismake.Bot(
    token=config.token,
    client_public_key=config.public_key,
    client_id=config.client_id,
    route="/",
)


@app.event()
async def on_ready():
    app.log.info("Logged in as %s" % app.user)
    await autocomplete.plugin.load(app)
    await mentions.plugin.load(app)
    await components.plugin.load(app)

    # sync = await app.sync_commands()
    # print(sync.text)




if __name__ == "__main__":
    app.run(app=f"main:app", reload=True)
