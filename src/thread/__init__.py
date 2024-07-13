"""
## Thread Library
Documentation at https://thread.ngjx.org/docs/2.0.5


---

Released under the BSD-3 License

Copyright (c) thread.ngjx.org, All rights reserved
"""

"""
This file contains the exports to
```py
import thread
```
"""

from .version import __version__

from . import _types as types
from . import exceptions

# Export decorators
from .decorators import processor, threaded

# Export Core
from .thread import ConcurrentProcessing, Thread

# Configuration
from .utils import Settings

# Wildcard Export
__all__ = [
    'Thread',
    'ConcurrentProcessing',
    'threaded',
    'processor',
    'types',
    'exceptions',
    'Settings',
    '__version__',
]
