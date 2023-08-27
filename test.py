import asyncio

import hikari


# This function will handle the interactions received
async def handle_command(interaction: hikari.CommandInteraction):
    # Create an initial response to be able to take longer to respond
    yield interaction.build_deferred_response()

    await asyncio.sleep(5)

    # Edit the initial response
    await interaction.edit_initial_response("Edit after 5 seconds!")


# Register the commands on startup.
#
# Note that this is not a nice way to manage this, as it is quite spammy
# to do it every time the bot is started. You can either use a command handler
# or only run this code in a script using `RESTApp` or add checks to not update
# the commands if there were no changes
async def create_commands(bot: hikari.RESTBot):
    application = await bot.rest.fetch_application()

    await bot.rest.set_application_commands(
        application=application.id,
        commands=[
            bot.rest.slash_command_builder("test", "My first test command!"),
        ],
    )


bot = hikari.RESTBot(
    token="...",
    token_type="...",
    public_key="...",
)

bot.add_startup_callback(create_commands)
bot.set_listener(hikari.CommandInteraction, handle_command)

from aiohttp import web_app

