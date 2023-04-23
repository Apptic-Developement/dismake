import dismake


house = dismake.House()

@house.button(label="1")
async def b1(ctx: dismake.ComponentContext):
    ...

@house.button(label="2")
async def b2(ctx: dismake.ComponentContext):
    ...

@house.button(label="3")
async def b3(ctx: dismake.ComponentContext):
    ...

@house.button(label="4")
async def b4(ctx: dismake.ComponentContext):
    ...

@house.button(label="5")
async def b5(ctx: dismake.ComponentContext):
    ...

@house.button(label="6")
async def b6(ctx: dismake.ComponentContext):
    ...

@house.button(label="7")
async def b7(ctx: dismake.ComponentContext):
    ...

@house.button(label="8")
async def b8(ctx: dismake.ComponentContext):
    ...

@house.button(label="9")
async def b9(ctx: dismake.ComponentContext):
    ...

@house.button(label="10")
async def b10(ctx: dismake.ComponentContext):
    ...




print(house.to_dict())
