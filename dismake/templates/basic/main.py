import dismake
import config
from plugins import misc


app = dismake.Bot(
    token=config.TOKEN, client_id=config.CLIENT_ID, client_public_key=config.PUBLIC_KEY
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

# Question: What does 'main:app' represent?
# Answer: 'main:app' represents the name of the main module
# and the variable or object within that module that will be used as the dismake.Bot.

# Question: Why is 'reload=True' included?
# Answer: The 'reload=True' parameter enables automatic reloading of the 
# uvicorn when changes are made to the code.
# This allows you to see the updates without manually restarting the server.
