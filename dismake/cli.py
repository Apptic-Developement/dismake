from __future__ import annotations

import typer
import shutil
import questionary
from typing import Optional
from pathlib import Path
from rich.prompt import Prompt
from rich.console import Console
from . import __version__

app = typer.Typer(name="dismake")
console = Console()


@app.command(name="version", help="Show version")
def help_command():
    console.print(f"[bold]Version[/bold]: {__version__}")

@app.command(name="init", help="Initialize a new project")
def init_command():
    project_name = Prompt.ask("[bold][cyan]?[/cyan] What is your project name", default="my-project")
    template_type = questionary.select(
        "Select a template type.",
        choices=["Basic", "Advance"],
    ).ask()

    path = Path(project_name)
    if path.is_file():
        console.log(f"[red]Error: [cyan]{project_name!r}[/cyan] is a file.")
    
    with console.status("[bold green]Working on tasks..."):
        try:
            shutil.copytree(f'dismake/templates/{str(template_type).lower()}/', path)
            console.log(f"[bold]Copied template: [bold cyan]Basic")
            console.log(f"[bold]Created template: [bold cyan]{project_name}")
        except FileExistsError:
            console.log(f"[red]Error: [cyan]{project_name!r}[/cyan] already exists.")

