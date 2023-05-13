import dismake
import config
from plugins import misc


app = dismake.Bot(
    token=config.TOKEN,
    client_id=config.CLIENT_ID,
    client_public_key=config.PUBLIC_KEY
)


@app.event()
async def on_ready():
    """This event is called when the bot is ready to recive interactions from discord."""
    misc.plugin.load(app)
    print("Logged in as %s" % app.user)

    # Sync all the slash commands to discord
    await app.sync_commands()


if __name__ == "__main__":
    app.run(app="main:app", reload=True)

# Question: What is 'main:app' ?
# Answer: the 'main' represents your main file name (The file you're providing python to run your bot).
# Question: Why 'reload=True' is there?
# Answer: It automatically reloads your bot when you make changes to your code.
