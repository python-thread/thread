"""
## Thread Library
Documentation at https://thread.ngjx.org/docs/2.0.1


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


__version__ = '2.0.1'


# Export Core
from .thread import Thread, ConcurrentProcessing


from . import _types as types, exceptions


# Export decorators
from .decorators import threaded, processor


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
