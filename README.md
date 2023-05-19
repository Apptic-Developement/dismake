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
import typing

app = dismake.Bot(...)

@app.event()
async def on_ready():
    print(f"Logged in as {app.user!r}.")

@app.command(
    name="echo",
    description="A simple echo command."
)
async def echo_command(
    ctx: dismake.Context,
    text: typing.Annotated[
        str, dismake.Option(name="text", description="Type something")
    ]
):
    await ctx.respond(f"{text}")

```
Explanation:
1. Import the `dismake` library to access its functionality.
2. Create a new instance of the `dismake.Bot` class, `app`, which will represent the connection to Discord. Replace ... with the necessary parameters, such as your bot token.
3. Use the `@app.event()` decorator to register an `on_ready` event. This event will be triggered when the bot successfully logs in to Discord. In this example, the event handler simply prints a message indicating that the bot has logged in.
4. Use the `@app.command()` decorator to register a slash command. In this case, the command is named "echo" and has a description of "A simple echo command."
5. Define the function `echo_command` to handle the "echo" command. The function takes two parameters: `ctx` (the dismake.Context object) and text (annotated with `typing.Annotated[str, dismake.Option(name="text", description="Type something")]`). The annotation provides additional information for the command option, specifying its name and description.
7. Inside the `echo_command` function, use the `ctx.respond` method to send a response back to the user. In this case, the response is the echoed text.

## 👨‍💻 Initialize and run.

To initialize a new dismake configuration file, follow these steps:

1. Open your console or terminal.
2. Run the command `dismake init`.
```bash
dismake init
```
3. You will be prompted with a question asking for the name of your bot variable.
```bash
? What is the name of your bot variable (app): app
```
4. Once you provide the bot variable name, dismake will generate a new file called `dismake.config.toml` for your project.
```bash
Successfully created a 'dismake.config.toml' file.
```
By following these steps, you will have successfully initialized a new dismake config file. 


To run the bot you need to run the following command in your console or terminal:
```
dismake run
```
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
