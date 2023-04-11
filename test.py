import dismake


house = dismake.House()

count: int = 0

@house.button(label="Click me")
async def click_me(ctx: dismake.ComponentContext):
    assert ctx.data is not None
    global count
    count += 1
    # await ctx.defer()

@house.button(label=str(count), style=dismake.ButtonStyles.secondary, disabled=True)
async def view_number(ctx: dismake.ComponentContext):
    ...

# print(house.to_dict())
