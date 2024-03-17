"""
## Thread Library
Documentation at https://thread.ngjx.org/docs/v1.1.1


---

Released under the GPG-3 License

Copyright (c) thread.ngjx.org, All rights reserved
"""

"""
This file contains the exports to
```py
import thread
```
"""


__version__ = '1.1.1'


# Export Core
from .thread import Thread, ParallelProcessing


from . import _types as types, exceptions


# Export decorators
from .decorators import threaded, processor


# Configuration
from .utils import Settings


# Wildcard Export
__all__ = [
    'Thread',
    'ParallelProcessing',
    'threaded',
    'processor',
    'types',
    'exceptions',
    'Settings',
    '__version__',
]
