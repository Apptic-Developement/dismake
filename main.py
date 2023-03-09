from fastapi import FastAPI, Request
from dismake import Client
from config import *
from dismake import Interaction, Option, OptionType
import uvicorn

from dismake.command import Choice

app = FastAPI()

dismake = Client(
    token=token, client_public_key=public_key, client_id=client_id, app=app
)

options: list[Option] = [
    Option(name="name", description="Enter your name"),
    Option(name="age", description="Enter your age"),
    Option(
        name="gender",
        description="Choose your gender",
        choices=[
            Choice(name="Male", value="male"),
            Choice(name="Female", value="Female"),
        ],
    ),
]


@dismake.command(
    name="command_name",
    description="Description of the command",
    options=options
)
async def callback(interaction: Interaction, name: str):
    pass

print(callback.to_dict())


@app.post("/interactions")
async def handle_interactions(request: Request):
    return await dismake.handle_interactions(request)
