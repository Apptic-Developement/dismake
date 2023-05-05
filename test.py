import typing as t
import inspect
from dismake import app_commands
from dismake.app_commands.commands import Option


def command(
    name: t.Annotated[
        str, app_commands.Option(name="name", description="This is name field")
    ],
    age: t.Annotated[
        int, app_commands.Option(name="age", description="This is age field")
    ],
    optional: str = "Hmm"
):
    ...


def validate_options(func: t.Callable):
    params = inspect.signature(command).parameters
    for k, v in params.items():
        """
        k: The name of the function
            - name
        v: The annotation of the function
            - typing.Annotated[str, <dismake.app_commands.commands.Option object at 0x7f050fade0d0>]
        """
        annotation = v.annotation
        if t.get_origin(annotation) != t.Annotated:
            continue
        option_type: type = annotation.__args__[0]
        option_object: Option = annotation.__metadata__[0]
        print(option_object.name)

validate_options(command)