from __future__ import annotations
import time
import typer
import shutil
import questionary
from pathlib import Path
from prompt_toolkit.styles import Style
from rich.console import Console
from . import __version__

app = typer.Typer(name="dismake")
console = Console()
default_styles_text = [
    ("qmark", "fg:#5f819d"),  # token in front of the question
    ("question", "bold"),  # question text
    ("answer", "fg:#00d9ff"),  # submitted answer text behind the question
    ("pointer", ""),  # pointer used in select and checkbox prompts
    ("selected", ""),  # style for a selected item of a checkbox
    ("separator", ""),  # separator in lists
    ("instruction", ""),  # user instructions for select, rawselect, checkbox
    ("text", ""),  # any other text
    ("instruction", "fg:#454545"),  # user instructions for select, rawselect, checkbox
]

default_styles_select = [
    ("qmark", "fg:#5f819d"),  # token in front of the question
    ("question", "bold"),  # question text
    ("answer", "fg:#00d9ff"),  # submitted answer text behind the question
    ("pointer", "fg:#00d9ff bold"),  # pointer used in select and checkbox prompts
    ("selected", ""),  # style for a selected item of a checkbox
    ("separator", ""),  # separator in lists
    ("instruction", ""),  # user instructions for select, rawselect, checkbox
    ("text", ""),  # any other text
    ("instruction", "fg:#454545"),  # user instructions for select, rawselect, checkbox
]



def generate_app(path: Path, template_type: str):
    template = Path(f"dismake/templates/%s" % template_type.lower())
    path.mkdir(parents=True, exist_ok=True)
    for item in template.iterdir():
        time.sleep(1)
        if item.is_file():
            shutil.copyfile(item, path / item.name)
        else:
            shutil.copytree(item, path / item.name)
        created_path = path / item.name
        console.print(f"[bold] :white_check_mark: Created {created_path.name!r}.")
    return True

@app.command(name="version", help="Show version")
def help_command():
    console.print(f"[bold]Version[/bold]: {__version__}")


@app.command(name="init", help="Initialize a new project")
def init_command():
    project_name = questionary.text(
        "Please enter a name for your project",
        style=Style(style_rules=default_styles_text),
        instruction="my-bot"
    ).ask()
    if project_name == "": project_name = "my-bot"
    template_type = questionary.select(
        "Choose a template type.",
        choices=["Basic", "Advance"],
        style=Style(style_rules=default_styles_select),
        pointer="➔",
    ).ask()

    try:
        path = Path(project_name)
    except Exception as e:
        return console.print(f"[red]Error: [cyan]{e.args[0]!r}[/cyan]")
    else:
        if path.is_file():
            console.log(f"[red]Error: [cyan]{project_name!r}[/cyan] is a file.")

        with console.status("[bold green]Creating your project..."):
            created = generate_app(path, template_type)
            if created:
                console.print("Done !!!", style="bold")
            # try:
            #     console.print(
            #         f"[bold]Creating project {project_name!r} using the {str(template_type).capitalize()!r} template..."
            #     )
            #     shutil.copytree(f"dismake/templates/{str(template_type).lower()}/", path)
            #     console.print(f"Done!!!", style="bold")
            # except FileExistsError:
            #     console.log(f"[red]Error: [cyan]{project_name!r}[/cyan] already exists.")
