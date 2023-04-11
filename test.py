import dismake

house = dismake.House()


@house.button(label="1")
async def c1(*_, **__):
    return


@house.button(label="2", style=dismake.ButtonStyles.danger)
async def c2(*_, **__):
    return


@house.button(label="3", style=dismake.ButtonStyles.secondary)
async def c3(*_, **__):
    return


@house.button(label="4", style=dismake.ButtonStyles.success)
async def c4(*_, **__):
    return


@house.button(label="5", url="https://www.google.com")
async def c5(*_, **__):
    return


# @house.button(label="6")
# async def c6(*_, **__):
#     return

# @house.button(label="7")
# async def c7(*_, **__):
#     return


# print(house.to_dict())
