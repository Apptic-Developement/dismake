from __future__ import annotations
from logging import getLogger
from functools import wraps
from typing import Optional
from fastapi import FastAPI
from .handler import InteractionHandler
from .app_commands.command import Option
from .types import AsyncFunction
from .types import SnowFlake
from .api import API
from .models import User, ApplicationCommand
from .app_commands import SlashCommand
from .utils import LOGGING_CONFIG

log = getLogger("uvicorn")


__all__ = ("Bot",)


class Bot(FastAPI):
    def __init__(
        self,
        token: str,
        client_public_key: str,
        client_id: int,
        route: str = "/interactions",
        **kwargs,
    ) -> None:
        super().__init__(**kwargs)
        self._client_id = client_id
        self._client_public_key = client_public_key
        self._interaction_handler = InteractionHandler(self)
        self._http = API(token=token, client_id=client_id)
        self.add_route(
            path=route,
            route=self._interaction_handler.handle_interactions,
            methods=["POST"],
            include_in_schema=False,
        )
        self.add_event_handler("startup", self._http.fetch_me)

    @property
    def user(self) -> User:
        return self._http._user

    def run(self, **kwargs):
        import uvicorn

        kwargs["log_config"] = kwargs.get("log_config", LOGGING_CONFIG)
        uvicorn.run(**kwargs)
