from __future__ import annotations

import shutil
import argparse
from pathlib import Path
from typing import Any


def generate_app(path: Path, template_type: str):
    template = Path(f"dismake/templates/%s" % template_type.lower())
    path.mkdir(parents=True, exist_ok=True)
    for item in template.iterdir():
        if item.is_file():
            shutil.copyfile(item, path / item.name)
        else:
            shutil.copytree(item, path / item.name)
    return True

def print_help(args):
    print("Help :)")

def init_command(args):
    # project_name = input("Please enter a name for your project: ")
    # try:
    #     path = Path(project_name)
    # except Exception as e:
    #     return print(f"TODO")
    # else:
    #     if path.is_file():
    #         print(f"A file already exists with this name.")
    #     created = generate_app(path, 'basic')
    #     if created:
    #         print("Done !!!")
    print("Okiee?")


def main():
    parser = argparse.ArgumentParser(prog="dismake", description='The command line interface for dismake library.',)
    subparsers = parser.add_subparsers()
    init = subparsers.add_parser("init", help="Create a new dismake project.")
    help = subparsers.add_parser("help", help="Shows help about dismake.")
    init.set_defaults(func=init_command)
    help.set_defaults(func=print_help)
    args = parser.parse_args()
    print(args)
    

if __name__ == '__main__':
    main()