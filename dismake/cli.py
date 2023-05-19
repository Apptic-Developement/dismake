from __future__ import annotations
import argparse
import json
import subprocess
from pathlib import Path
from pydantic import ValidationError
from rich.console import Console
from rich.prompt import Prompt
from .internal import Config




console = Console()
config_file = "dismake.config.toml"


def print_help(parser: argparse.ArgumentParser):
    parser.print_help()


def init_command(args: argparse.Namespace):
    path = Path(".") / config_file
    try:
        Config.get_config(path)
    except:
        var: str = Prompt.ask("[bold][cyan]?[/cyan][/bold] [bold]What is the name of your bot variable[/bold]", default="app")
        console.clear()
        Config.create_config(path, var=var)
    else:
        return console.print(
            f"A {config_file!r} file already exists.", style="bold"
        )

    return console.print(f"Successfully created a {config_file!r} file.", style="bold")

def run_command(args: argparse.Namespace):
    path = Path(".") / config_file

    if not path.exists():
        console.print(f"Creating {config_file!r}", style="bold red")
        init_command(args)
    if not Config.can_load(path):
        console.print(f"Found syntax error in {config_file!r}", style="bold red")
        init_command(args)
    try:
        config = Config.get_config(path)
    except ValidationError as ve:
        error_messages = ()
        for error in ve.errors():
            field = error['loc'][0]
            message = error['msg']
            error_messages += (f"Field {field!r} has error: {message}", )
        return console.print("\n".join(error_messages), style="bold red")
    except ValueError as e:
        return console.print(f"{e.args[0]}", style="bold red")
    else:
        exc_command = ["uvicorn", f"{config.dismake.main_file_name}:{config.dismake.bot.var}"]
        if config.dismake.auto_reload:
            exc_command.append("--reload")
        subprocess.run(exc_command)


def vercel_command(args):
    path = Path(".") / "vercel.json"
    config = {
        "builds": [{"src": "<your-main-file>", "use": "@vercel/python"}],
        "routes": [{"src": "/(.*)", "dest": "your-main-file"}],
    }
    path.touch()
    with open(path, "w") as f:
        f.write(json.dumps(config))
    console.print(
        """Successfully created a 'vercel.json' file.
Replace the '<your-main-file>' with your main file name example 'main.py'."""
    )


def add_subparsers(parser):
    subparsers = parser.add_subparsers()
    vercel = subparsers.add_parser(
        "vercel", help="Generate a vercel.json file for deployment on vercel."
    )
    vercel.set_defaults(func=vercel_command)

    init = subparsers.add_parser(
    "init", help="Initialize a new config.toml file."
    )
    init.set_defaults(func=init_command)

    run = subparsers.add_parser(
        "run", help="Run your bot."
    )
    run .set_defaults(func=run_command)
    return subparsers


def main():
    parser = argparse.ArgumentParser(
        prog="dismake",
        description="The command line interface for dismake library.",
    )
    add_subparsers(parser)
    args = parser.parse_args()
    if not bool(args._get_kwargs()):
        return print_help(parser)
    return args.func(args)


if __name__ == "__main__":
    main()
