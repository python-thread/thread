"""
## Types

Documentation: https://thread.ngjx.org
"""

from typing import Any, Literal, Callable, Union

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

HookFunction = Callable[[Data_Out], Union[Any, None]]
