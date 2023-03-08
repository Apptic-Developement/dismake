from fastapi import FastAPI, Request
from dismake import Client, SlashCommand, Option, SlashCommand
from config import *
from dismake.models.command import SubCommand


app = FastAPI()

client = Client(
    token=token,
    client_public_key=public_key,
    client_id=client_id,
    app=app
)

giveaway = SlashCommand(
    name="giveaway",
    description="Giveaway a bra with free panty for goa trip.")

start = SubCommand(
    parent=giveaway,
    name="start",
    description="Starts a bra's giveaway."
)
@client.listen(start)
async def callback(*args):
    pass


@app.post("/interactions")
async def handle_interactions(request: Request):
    return await client.handle_interactions(request)

