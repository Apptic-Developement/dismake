from dismake import Command, Option, Choice

command = Command(
    name="Hehe",
    options=[
        Option(name="o1")
    ]
)
command = command.json(exclude_none=True)
print(command)