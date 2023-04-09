from __future__ import annotations
from typing import TYPE_CHECKING
from dismake import SlashCommand, Context
if TYPE_CHECKING:
    from dismake import Bot
class InfoCommand(SlashCommand):
    def __init__(self, bot: Bot):
        super().__init__(name="info", description="Info about the dismake bot.")
        self.bot = bot

    async def callback(self, ctx: Context):
        guild = await ctx.fetch_guild()
        await ctx.respond(guild.name)
#         return await ctx.respond(
#             f"""Hello! I'm a testing bot for the **dismake** library, a Python wrapper for the Discord Interaction API based on FastAPI. Our library is currently under development, but we're excited to bring you a powerful and user-friendly tool for creating interactive bots on Discord.

# To answer your question, we're currently hosted on Vercel, a cloud platform that provides serverless functions and static sites. This allows us to easily deploy and scale our code, so we can focus on building great features for our users.

# If you're interested in learning more about dismake or contributing to our project, check out our GitHub repository at <https://github.com/PranoyMajumdar/dismake>. We'd love to hear your feedback and ideas for making dismake even better.

# Thanks for using our bot, and happy bot-making!

#             """
#         )
