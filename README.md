# Introduction to Dismake

<p align="center">
  <img src="/docs/public/logo.png" alt="Dismake Logo"  style="border-radius:50%"/>
   <a href="https://pypi.org/project/dismake/">
   <img src="https://badge.fury.io/py/dismake.svg" alt="Pypi v" />
   </a>
</p>

[Dismake](https://github.com/PranoyMajumdar/dismake) is a robust framework designed to assist you in developing stateless and independent Discord bots that employ Slash Commands. The framework is built on top of the [FastAPI](https://fastapi.tiangolo.com), a high-performance Python web framework, making it easy to use, efficient, and speedy.

## ☢️ Prerequisites
- Dismake requires Python 3.9 or later versions to work correctly. 
- Discord Bot token 

## 🏁 Getting Started with Dismake
Before you start using Dismake, you'll need to create a new Discord application and add a bot to it.

### 💻 Installing
To install Dismake, use the following command to install it directly from PyPI:
```bash
pip install dismake
```

## 🤖 Creating a Minimal Discord Bot with Dismake
Let's create a basic bot that echoes user text back to them.

Create a new Python file named `main.py`, and copy and paste the following code:

```py
import dismake
from dismake import commands
import typing

app = dismake.Bot(...)

@app.event('ready')
async def ready_event():
    print(f"Logged in as {app.user}.")

@app.command(
    name="echo",
    description="A simple echo command."
)
async def echo_command(
    ctx: dismake.Context, 
    text: typing.Annotated[
        str,
        commands.Option(name="text", description="Type something"), type=str
    ]
):
    await ctx.respond(f"{text}")

if __name__ == "__main__":
    app.run(app="main:app", reload=True)
 ```

The code above demonstrates how to use Dismake to create a basic Discord bot that responds to slash commands.

Here's a brief explanation of what each part of the code does:

- The first line imports the Dismake library. Make sure you've installed Dismake before you run the code.
- Next, we create a new instance of the `Dismake.Bot` class, which serves as our connection to Discord.
- We register an event using the `Dismake.Bot.event()` decorator. This library provides numerous events, and we use this callback to perform asynchronous operations once the bot is logged in.
- We register a slash command using the `Dismake.Bot.command()` decorator. This decorator requires the command's name and description as arguments.
- In the function that handles the command, we use the Dismake.Context object to interact with Discord. We take the user's input text and echo it back to them.
- Finally, we use the `app.run()` method to start the bot. We've named our bot app in this example. The second argument, `reload=True`, instructs Uvicorn to reload the app automatically when changes are made to the code.

To run the bot, open the terminal, navigate to the directory containing `main.py`, and enter the following command:

```bash
python main.py
```

> You can now experiment with your basic bot.

## ✨ Features

- Easy-to-use and intuitive framework for building Discord bots with Slash Commands
- Built on top of the FastAPI web framework, providing a high-performance and efficient backend
- Fully customizable with support for middleware, extensions, and custom context classes
- Supports easy integration with databases, message queues, and other external services
- Provides a convenient and powerful way to define and manage Slash Commands and their options
- Includes built-in command validation and error handling for cleaner and more maintainable code

## 📖 Documentation

For detailed usage and installation instructions, please check out the official [Dismake documentation](/docs/pages/index.mdx)

## 🏥 Support

If you have any questions or issues with Dismake, please feel free to reach out to us on the [Discord server](https://discord.gg/your-discord-server-link-here).

## 🗺️ Roadmap

For details about our roadmap, please check out our [Roadmap page](/docs/pages/roadmap.mdx).

## 🤝 Contributing
We welcome contributions from anyone! If you want to contribute to Dismake, please follow these guidelines:

#### • Contributing to the Documentation
The documentation is generated with [Nextra](https://github.com/shuding/nextra). If you want to contribute to the documentation, please do the following:

1. Clone the repository.
2. Navigate to the `/docs` directory.
3. Run `npm install` to install the required dependencies.
4. Run `npm run dev` to start the development server.
5. Make your changes, push and create a pull request.

#### • Contributing to the Dismake Package
If you want to contribute to the Dismake package or report an issue, please do the following:

1. Fork the repository.
2. Make your changes.
3. Format your code 
4. Test your code & push.
5. Create a pull request.

Thank you for contributing!

## 🪪 License

Dismake is released under the [MIT License](https://opensource.org/licenses/MIT). See the [LICENSE](https://github.com/PranoyMajumdar/dismake/blob/main/LICENSE) file for more details.
