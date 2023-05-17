from __future__ import annotations
import argparse
import json
from pathlib import Path

# def generate_app(path: Path):
#     template = Path(pkg_resources.resource_filename("dismake", "templates"))
#     if not template.exists():
#         return print(
#             f"""
#     Error
# =============
# The templates folder is missing.
# You can fix this issue by reinstalling the package.

# Command:
# pip uninstall dismake -y && pip install dismake
# """
#         )
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
#         created = generate_app(path, "basic")
#         if created:
#             return print(
#                 f"Successfully created your project in {created.absolute().name!r}"
#             )


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
        """Successfully created a 'vercel.json' file.
Replace the '<your-main-file>' with your main file name example 'main.py'."""
    )


def add_subparsers(parser):
    subparsers = parser.add_subparsers()
    vercel = subparsers.add_parser(
        "vercel", help="Generate a vercel.json file for deployment on vercel."
    )
    vercel.set_defaults(func=vercel_command)

    # init = subparsers.add_parser(
    # "init", help="Creates a new dismake project for you."
    # )
    # init.set_defaults(func=init_command)
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
