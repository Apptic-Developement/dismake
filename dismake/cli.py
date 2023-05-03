from __future__ import annotations

import typer
from typing import Annotated, Optional
from pathlib import Path
from rich.prompt import Prompt
from rich.console import Console


app = typer.Typer(name="dismake")
console = Console()


def make_prompt_text(text: str, default: Optional[str]):
    if default:
        return f"[bold][cyan]?[/cyan] {text} [black]({default})[/black][/bold]"
    return f"[cyan]?[/cyan] {text}"

@app.command(name="init")
def init_command(path: Optional[Path] = Path(".")):
    assert path is not None, "Path doesn't exists."
    project_name = Prompt.ask(make_prompt_text("What is your project name", "my-project"))     
@app.command(name="sync")
def sync_command():
    console.print("[bold][red]Sync command is still in developement.[/red][/bold]")
