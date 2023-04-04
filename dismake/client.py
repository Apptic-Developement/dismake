from __future__ import annotations
import asyncio

from logging import getLogger
from functools import wraps
from typing import List, Dict
from fastapi import FastAPI
from .handler import InteractionHandler
from .types import AsyncFunction
from .api import API
from .models import User
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
        self._events: Dict[str, List[AsyncFunction]] = {}
        self.add_event_handler('startup', lambda : self.dispatch('ready'))



    @property
    def user(self) -> User:
        return self._http._user

    def run(self, **kwargs):
        import uvicorn
        kwargs["log_config"] = kwargs.get("log_config", LOGGING_CONFIG)
        uvicorn.run(**kwargs)

    
    async def _dispatch_callback(self, coro: AsyncFunction, *args, **kwargs):
        try:
            await coro(*args, **kwargs)
        except Exception as e:
            log.error("An error occured in %s" % coro.__name__, exc_info=e)

    def dispatch(self, event_name: str, *args, **kwargs):
        event = self._events.get(event_name)
        if not event:
            return
        for coro in event:
            asyncio.ensure_future(self._dispatch_callback(coro, *args, **kwargs))

    def event(self, event_name: str):
        def decorator(coro: AsyncFunction):
            @wraps(coro)
            def wrapper(*_, **__):
                if self._events.get(event_name) is not None:
                    self._events[event_name].append(coro)
                else:
                    self._events[event_name] = [coro]
            return wrapper()
        return decorator
                    
    
    
