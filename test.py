import dismake, random
from dismake import ui

house = ui.House()

setattr(house, 'count', 0)
@house.button(label="Click", custom_id="random_number_gusser")
async def click_me(ctx: dismake.ComponentContext):
    setattr(house, 'count', getattr(house, 'count') + 1)
    view.label = getattr(house, 'count')
    await ctx.edit_message(f"Click to increase count.", house=house)

@house.button(label=f"{getattr(house, 'count')}", disabled=True)
async def view(ctx: dismake.ComponentContext):
    ...

# @house.button(label="3")
# async def b3(ctx: dismake.ComponentContext):
#     ...

# @house.button(label="4")
# async def b4(ctx: dismake.ComponentContext):
#     ...

# @house.button(label="5")
# async def b5(ctx: dismake.ComponentContext):
#     ...

# @house.button(label="6")
# async def b6(ctx: dismake.ComponentContext):
#     ...

# @house.button(label="7")
# async def b7(ctx: dismake.ComponentContext):
#     ...

# @house.button(label="8")
# async def b8(ctx: dismake.ComponentContext):
#     ...

# @house.button(label="9")
# async def b9(ctx: dismake.ComponentContext):
#     ...

# @house.button(label="10")
# async def b10(ctx: dismake.ComponentContext):
#     ...



# @house.button(label="11")
# async def b11(ctx: dismake.ComponentContext):
#     ...

# @house.button(label="12")
# async def b12(ctx: dismake.ComponentContext):
#     ...

# @house.button(label="13")
# async def b13(ctx: dismake.ComponentContext):
#     ...

# @house.button(label="14")
# async def b14(ctx: dismake.ComponentContext):
#     ...

# @house.button(label="15")
# async def b15(ctx: dismake.ComponentContext):
#     ...

# @house.button(label="16")
# async def b16(ctx: dismake.ComponentContext):
#     ...

# @house.button(label="17")
# async def b17(ctx: dismake.ComponentContext):
#     ...

# @house.button(label="18")
# async def b18(ctx: dismake.ComponentContext):
#     ...

# @house.button(label="19")
# async def b19(ctx: dismake.ComponentContext):
#     ...

# @house.button(label="20")
# async def b20(ctx: dismake.ComponentContext):
#     ...


# @house.button(label="21")
# async def b21(ctx: dismake.ComponentContext):
#     ...

# @house.button(label="22")
# async def b22(ctx: dismake.ComponentContext):
#     ...

# @house.button(label="23")
# async def b23(ctx: dismake.ComponentContext):
#     ...

# @house.button(label="24")
# async def b24(ctx: dismake.ComponentContext):
#     ...

# @house.button(label="25")
# async def b25(ctx: dismake.ComponentContext):
#     ...

# print(house)