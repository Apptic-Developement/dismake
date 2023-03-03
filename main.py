from fastapi import FastAPI, Request
from dismake import Client

app = FastAPI()
client = Client(
    token="MTA3MTg1MTMyNjIzNDk1MTc3MA.GXGfcE.cTAgTPOnN0sRe7UaBHsrCMp_3n-J9k253DOBFs",
    client_public_key="9b11aa01a931bd060cc43b3a0a7a51833734828978e1d19026b61e5d01b15b10",
    client_id=1071851326234951770,
    app=app
)

