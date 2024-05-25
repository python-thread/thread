"""
## Types
"""

from typing import Any, Literal, Callable, Union, Sized
from typing_extensions import (
    ParamSpec,
    TypeVar,
    Concatenate,
    Protocol,
    runtime_checkable,
)


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

_Dataset_T = TypeVar('_Dataset_T', covariant=True)
DatasetFunction = Callable[Concatenate[_Dataset_T, _Target_P], _Target_T]


# Protocols
@runtime_checkable
class SupportsLength(Sized, Protocol):
    pass


_SupportsGetItem_T = TypeVar('_SupportsGetItem_T')


@runtime_checkable
class SupportsGetItem(Protocol[_SupportsGetItem_T]):
    __getitem__: Callable[..., _SupportsGetItem_T]


# Looks like having this inherit __getitem__ from SupportsGetItem breaks isinstance checks in python3.12
# Thus we explicitly define it
@runtime_checkable
class SupportsLengthGetItem(Sized, Protocol[_SupportsGetItem_T]):
    __getitem__: Callable[..., _SupportsGetItem_T]


LengthLike_T = TypeVar('LengthLike_T', bound=SupportsLength)
GetLike_T = TypeVar('GetLike_T', bound=SupportsGetItem)
LengthandGetLike_T = TypeVar('LengthandGetLike_T', bound=SupportsLengthGetItem)
