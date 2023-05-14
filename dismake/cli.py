from __future__ import annotations

import argparse
import json
from pathlib import Path


# def generate_app(path: Path, template_type: str):
#     template = Path(f"dismake/templates/%s" % template_type.lower())
#     path.mkdir(parents=True, exist_ok=True)
#     for item in template.iterdir():
#         if item.is_file():
#             shutil.copyfile(item, path / item.name)
#         else:
#             shutil.copytree(item, path / item.name)
#     return path


def print_help(parser: argparse.ArgumentParser):
    parser.print_help()


# def init_command(args: argparse.Namespace):
#     project_name = input("Please enter a name for your project: ")
#     try:
#         path = Path(project_name)
#     except Exception as e:
#         return print(f"TODO")
#     else:
#         if path.is_file():
#             print(f"A file already exists with this name.")
#         created = generate_app(path, 'basic')
#         if created:
#             print(created)


def vercel_command(args):
    path = Path(".") / "vercel.json"
    config = {
        "builds": [{"src": "<your-main-file>", "use": "@vercel/python"}],
        "routes": [{"src": "/(.*)", "dest": "your-main-file"}],
    }
    path.touch()
    with open(path, "w") as f:
        f.write(json.dumps(config))
    print(
        f"""Successfully created a 'vercel.json' file.
Replace the '<your-main-file>' with your main file name example 'main.py'."""
    )


def add_subparsers(parser):
    subparsers = parser.add_subparsers()
    vercel = subparsers.add_parser(
        "vercel", help="Generate a vercel.json file for deployment on vercel."
    )
    vercel.set_defaults(func=vercel_command)
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
