from __future__ import annotations

import typer
from typing import Annotated, Optional
from pathlib import Path
from rich.prompt import Prompt
from rich.console import Console
from . import __version__

app = typer.Typer(name="dismake")
console = Console()


def make_prompt_text(text: str, default: Optional[str]):
    if default:
        return f"[bold][cyan]?[/cyan] {text} [black]({default})[/black][/bold]"
    return f"[cyan]?[/cyan] {text}"

@app.command(name="version", help="Show version")
def help_command():
    console.print(f"[bold]Version[/bold]: {__version__}")

@app.command(name="init", help="Initialize a new project")
def init_command():
    project_name = Prompt.ask(
        make_prompt_text("What is your project name", "my-project")
    )
    if not project_name:
        return console.print(f"[red]Error: [cyan]{project_name!r}[/cyan] is empty.")
        
    path = Path(project_name)
    if path.is_file():
        console.print(f"[red]Error: [cyan]{project_name!r}[/cyan] is a file.")
    elif not path.exists():
        console.print(f"Creating your project: [cyan]{project_name!r}[/cyan]")


