from typing import Annotated
from dismake import ui, Interaction

modal = ui.Modal(title="Okiee?")


@modal.on_submit
async def callback(
    interaction: Interaction,
    o1: Annotated[str, ui.TextInput()],
    o2: Annotated[str, ui.TextInput()],
    o3: Annotated[str, ui.TextInput()],
    o4: Annotated[str, ui.TextInput()],
    o5: Annotated[str, ui.TextInput()],
):
    ...


print(modal.to_dict())
# from dismake import AsyncFunction
# from dismake.models.interaction import Interaction
# from dismake.ui import TextInput
# import inspect
# from typing import get_origin, Annotated

# def _get_text_inputs(coro) -> list[TextInput]:
#     inputs: list[TextInput] = list()
#     parameters = inspect.signature(coro).parameters
#     for k, v in parameters.items():
#         # k: name of the parameter
#         # v: Annotation of the parameter
#         annotation: Annotated = v.annotation
#         if get_origin(annotation) == Annotated:
#             text_input: TextInput = annotation.__metadata__[0]
#             input_type: type = annotation.__args__[0]
#             if input_type not in (str, int, float, bool):
#                 raise ValueError(
#                     f"Text input can only support 'str, int, float, bool' types not {input_type.__name__!r}"
#                 )
#             text_input.type = input_type
#             if text_input.label is None:
#                 text_input.label = k
#             if v.default != inspect._empty:
#                 text_input.value = v.default
            
#             inputs.append(text_input)
#     return inputs

# def modal(
#     interaction: Interaction,
#         o1: Annotated[str, TextInput()],
#     o2: Annotated[str, TextInput()],
#     o3: Annotated[str, TextInput()],
#     o4: Annotated[str, TextInput()],
#     o5: Annotated[str, TextInput()] = "Ok",
# ):
#     ...

# print((_get_text_inputs(modal)))