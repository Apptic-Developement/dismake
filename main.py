from typing import Annotated
import dismake, config
from plugins import group
from dismake.app_commands import Option

app = dismake.Bot(
    token=config.token,
    client_public_key=config.public_key,
    client_id=config.client_id,
    route="/",
)

group.plugin.load(app)


@app.event("ready")
async def on_ready():
    print("Logged in as %s" % app.user)
    # sync = await app.sync_commands()
    # print(sync.text)




if __name__ == "__main__":
    app.run(app=f"main:app", reload=True)
