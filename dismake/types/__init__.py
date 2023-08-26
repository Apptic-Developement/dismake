from .user import *
from .member import *
from .role import *
from .snowflake import *
from .undefined import *
from .guild import *

from typing import Any, Callable, Coroutine


AsyncFunction = Callable[[], Coroutine[Any ,Any, Any]]