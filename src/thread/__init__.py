"""
## Thread Library
Documentation at https://thread.ngjx.org


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


# Export Core
from .thread import (
  Thread,
  ParallelProcessing
)


from . import (
  _types as types,
  exceptions
)

# Configuration
from .utils import Settings
