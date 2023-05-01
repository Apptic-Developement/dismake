from .snowflake import *
from .interactions import *
from .user import *
from .role import *
from .undefined import *

from collections.abc import Coroutine
from typing import Any, Callable


AsyncFunction = Callable[..., Coroutine[Any, Any, Any]]
