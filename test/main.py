import config
import dismake
from plugins import autocomplete, components, mentions

# mypy --show-error-codes --pretty --check-untyped-defs dismake

app = dismake.Bot(
    token=config.token,
    client_public_key=config.public_key,
    client_id=config.client_id,
    route="/",
)


@app.event()
async def on_ready():
    print("Logged in as %s" % app.user)
    await autocomplete.plugin.load(app)
    await mentions.plugin.load(app)
    await components.plugin.load(app)

    # sync = await app.sync_commands()
    # print(sync.text)

