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
    name="test_command",
    description="Description of the command",
)
async def test_command(interaction: Interaction, name: str):
    pass


@test_command.subcommand(
    name="test_sub_command",
    description="This is a sub command",
    options=options
)
async def test_sub_command(interaction: Interaction, name: str):
    pass

print(test_command.to_dict())


@app.post("/interactions")
async def handle_interactions(request: Request):
    return await dismake.handle_interactions(request)
