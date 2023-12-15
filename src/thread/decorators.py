"""
## Decorators

Documentation: https://thread.ngjx.org
"""

import inspect
from functools import wraps, partial
from abc import ABC, abstractmethod

from ._types import Overflow_In, Data_Out, Data_In
from typing import Any, Callable, Mapping, Tuple, Sequence, Optional, Union, Protocol, Iterable, overload
from typing_extensions import ParamSpec, TypeVar, Concatenate

from .thread import Thread
from .exceptions import AbstractInvokationError, ArgumentValidationError


T = TypeVar('T')
P = ParamSpec('P')
TargetFunction = Callable[P, Data_Out]
NoParamReturn = Callable[P, Thread]
WithParamReturn = Callable[[TargetFunction], NoParamReturn]
FullParamReturn = Callable[P, Thread]
WrappedWithParamReturn = Callable[[TargetFunction], WithParamReturn]


@overload
def threaded(__function: TargetFunction) -> NoParamReturn: ...

@overload
def threaded(
  *,
  args: Sequence[Data_In] = (),
  kwargs: Mapping[str, Data_In] = {},
  ignore_errors: Sequence[type[Exception]] = (),
  suppress_errors: bool = False,
  **overflow_kwargs: Overflow_In
) -> WithParamReturn: ...

@overload
def threaded(
  __function: Callable[P, Data_Out],
  *,
  args: Sequence[Data_In] = (),
  kwargs: Mapping[str, Data_In] = {},
  ignore_errors: Sequence[type[Exception]] = (),
  suppress_errors: bool = False,
  **overflow_kwargs: Overflow_In
) -> FullParamReturn: ...


def threaded(
  __function: Optional[TargetFunction] = None,
  *,
  args: Sequence[Data_In] = (),
  kwargs: Mapping[str, Data_In] = {},
  ignore_errors: Sequence[type[Exception]] = (),
  suppress_errors: bool = False,
  **overflow_kwargs: Overflow_In
) -> Union[NoParamReturn, WithParamReturn, FullParamReturn]:
  """
  test 1
  """

  if not callable(__function):
    def wrapper(func: TargetFunction) -> FullParamReturn:
      return threaded(
        func,
        args = args,
        kwargs = kwargs,
        ignore_errors = ignore_errors,
        suppress_errors = suppress_errors,
        **overflow_kwargs
      )
    return wrapper

  overflow_kwargs.update({
    'ignore_errors': ignore_errors,
    'suppress_errors': suppress_errors
  })

  kwargs = dict(kwargs)
  
  @wraps(__function)
  def wrapped(*parsed_args: P.args, **parsed_kwargs: P.kwargs) -> Thread:
    """test 2"""
    kwargs.update(parsed_kwargs)

    processed_args = ( *args, *parsed_args )
    processed_kwargs = { i:v for i,v in kwargs.items() if i not in ['args', 'kwargs'] }

    job = Thread(
      target = __function,
      args = processed_args,
      kwargs = processed_kwargs,
      **overflow_kwargs
    )
    job.start()
    return job
  
  return wrapped
