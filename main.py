import dismake, config

app = dismake.Bot(
    token=config.token,
    client_public_key=config.public_key,
    client_id=config.client_id
)
