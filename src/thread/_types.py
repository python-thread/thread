"""
## Types

Documentation: https://thread.ngjx.org
"""

from typing import Any, Literal, Callable, Union


# Descriptive Types
Data_In = Any
Data_Out = Any
Overflow_In = Any


# Variable Types
ThreadStatus = Literal[
  'Idle',
  'Running',
  'Invoking hooks',
  'Completed',

  'Errored',
  'Kill Scheduled',
  'Killed'
]


# Function types
HookFunction = Callable[[Data_Out], Union[Any, None]]
TargetFunction = Callable[..., Data_Out]
