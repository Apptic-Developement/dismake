from fastapi import FastAPI, Request
from dismake import Client
from config import *
from dismake.command import SlashCommand, Option
from dismake import Interaction
from dismake.types.command import OptionType
import uuid
app = FastAPI()

dismake = Client(
    token=token,
    client_public_key=public_key,
    client_id=client_id,
    app=app
)


@dismake.command(name="command_name",description="Description of the command")
async def test_collback(interaction: Interaction,name: Option(name="ok", description="Okkk")):
    pass


print(dismake._slash_commands)


@app.post("/interactions")
async def handle_interactions(request: Request):
    return await dismake.handle_interactions(request)


