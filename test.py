import toml
from pydantic import BaseModel


class BotConfig(BaseModel):
    var: str
    token_name: str
    load_env: bool


class DismakeConfig(BaseModel):
    autoreload: bool
    bot: BotConfig


class Config(BaseModel):
    dismake: DismakeConfig


with open("test.toml", "r") as file:
    config = Config(**toml.load(file))

print(config.dismake.bot.var)
