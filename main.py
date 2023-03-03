from fastapi import FastAPI, Request
from dismake import Client
from config import *


app = FastAPI()
client = Client(
    token=token,
    client_public_key=public_key,
    client_id=client_id,
    app=app
)

@app.post("/interactions")
async def handle_interactions(request: Request):
    return await client.handle_interactions(request)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app="main:app",
        access_log=False,
        reload=True,

    )