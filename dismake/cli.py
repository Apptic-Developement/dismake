from __future__ import annotations

import shutil
import argparse
from pathlib import Path


def generate_app(path: Path, template_type: str):
    template = Path(f"dismake/templates/%s" % template_type.lower())
    path.mkdir(parents=True, exist_ok=True)
    for item in template.iterdir():
        if item.is_file():
            shutil.copyfile(item, path / item.name)
        else:
            shutil.copytree(item, path / item.name)
    return path

def print_help(parser: argparse.ArgumentParser):
    parser.print_help()

def init_command(args: argparse.Namespace):
    project_name = input("Please enter a name for your project: ")
    try:
        path = Path(project_name)
    except Exception as e:
        return print(f"TODO")
    else:
        if path.is_file():
            print(f"A file already exists with this name.")
        created = generate_app(path, 'basic')
        if created:
            print(created)


def main():
    parser = argparse.ArgumentParser(prog="dismake", description='The command line interface for dismake library.',)
    subparsers = parser.add_subparsers()
    init = subparsers.add_parser("init", help="Create a new dismake project.")
    init.set_defaults(func=init_command)
    args = parser.parse_args()
    if not bool(args._get_kwargs()):
        return print_help(parser)
    return args.func(args)
    

if __name__ == '__main__':
    main()