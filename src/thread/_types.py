"""
## Types

Documentation: https://thread.ngjx.org
"""

from typing import Any, Literal

ThreadStatus = Literal[
  'Idle',
  'Running',
  'Invoking hooks',
  'Completed',

  'Errored',
  'Kill Scheduled',
  'Killed'
]
Data_In = Any
Data_Out = Any
Overflow_In = Any
