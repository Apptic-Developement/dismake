from discord import ui
from discord.ext import commands
import discord, config

bot = commands.Bot(
    command_prefix="!",
    intents=discord.Intents.none()
)



class MyView(ui.View):
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(ui.Button(label="Ok1"))
        self.add_item(ui.Button(label="Ok2"))
        self.add_item(ui.Button(label="Ok3"))
        self.add_item(ui.Button(label="Ok4"))
        self.add_item(ui.Button(label="Ok5"))
        self.add_item(ui.Button(label="Ok6"))
        self.add_item(ui.Button(label="Ok7"))
        self.add_item(ui.Button(label="Ok8"))
        self.add_item(ui.Button(label="Ok9"))
        self.add_item(ui.Button(label="Ok10"))

@bot.event
async def on_ready():
    print(MyView().to_components())


bot.run(config.token)