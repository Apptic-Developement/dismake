from .interactions import *
from .command import *
from .dicts import *
from .snowflake import *


from collections.abc import Coroutine
from typing import Any, Awaitable, Callable
AsyncFunction = Callable[..., Coroutine[Any, Any, Any]]

