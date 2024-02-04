"""
## Types

Documentation: https://thread.ngjx.org
"""

from typing import Any, Literal, Callable, Union
from typing_extensions import ParamSpec, TypeVar


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
'Killed',
]


# Function types
_Target_P = ParamSpec('_Target_P')
_Target_T = TypeVar('_Target_T')
TargetFunction = Callable[_Target_P, _Target_T]

HookFunction = Callable[[_Target_T], Union[Any, None]]

_Dataset_T = TypeVar('_Dataset_T')
DatasetFunction = Callable[[_Dataset_T], _Target_T]
