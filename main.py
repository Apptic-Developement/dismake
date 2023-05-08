import dismake, config
from plugins import mentions, components, autocomplete

app = dismake.Bot(
    token=config.token,
    client_public_key=config.public_key,
    client_id=config.client_id,
    route="/",
)

mentions.plugin.load(app)
components.plugin.load(app)
autocomplete.plugin.load(app)


@app.event("ready")
async def on_ready():
    print("Logged in as %s" % app.user)
    # sync = await app.sync_commands()
    # print(sync.text)


if __name__ == "__main__":
    app.run(app=f"main:app", reload=True)
m = {
    "app_permissions": "140737488355327",
    "application_id": "1071851326234951770",
    "channel": {
        "flags": 0,
        "guild_id": "882441738713718815",
        "id": "1070755073866616865",
        "last_message_id": "1104798917960413335",
        "name": "│chat",
        "nsfw": False,
        "parent_id": "997068127907090442",
        "permissions": "140737488355327",
        "position": 11,
        "rate_limit_per_user": 0,
        "topic": None,
        "type": 0,
    },
    "channel_id": "1070755073866616865",
    "data": {
        "id": "1104011347341094932",
        "name": "mentions",
        "options": [
            {
                "name": "autocomplete",
                "options": [
                    {"name": "fav_fruit", "type": 3, "value": "ok"},
                    {"name": "fav_fruit2", "type": 3, "value": "hmm"},
                    {"focused": True, "name": "fav_fruit3", "type": 3, "value": ""},
                ],
                "type": 1,
            }
        ],
        "type": 1,
    },
    "entitlement_sku_ids": [],
    "entitlements": [],
    "guild_id": "882441738713718815",
    "guild_locale": "en-US",
    "id": "1104822090537914481",
    "locale": "en-GB",
    "member": {
        "avatar": None,
        "communication_disabled_until": None,
        "deaf": False,
        "flags": 0,
        "joined_at": "2022-02-18T06:07:45.873000+00:00",
        "mute": False,
        "nick": None,
        "pending": False,
        "permissions": "140737488355327",
        "premium_since": None,
        "roles": ["1070758821573693624", "1071341486702088193", "1071340327287390248"],
        "user": {
            "avatar": "afabeeecc85fafcc1100709481824350",
            "avatar_decoration": None,
            "discriminator": "0140",
            "display_name": None,
            "global_name": None,
            "id": "942683245106065448",
            "public_flags": 4194560,
            "username": "Pranoy",
        },
    },
    "token": "aW50ZXJhY3Rpb246MTEwNDgyMjA5MDUzNzkxNDQ4MTpkSlZTWXBBNDlmSUViRGRnbGhYNjFaOENYdmoxb1dtdEhKRkJDZFNKZE5YNTk1WmlyVjljUG4waUYxMExvN1o1a1NNeUl0Z3l5bE4wemh5TFZET2U1aVk2bGRQOVlKUUd0N1lKR1g2OVp1SlJMYzdqbFlSWU5jZTRQam85dExJUw",
    "type": 4,
    "version": 1,
}
