"""
## Processor
"""

from functools import wraps
from ..thread import ConcurrentProcessing

from .._types import (
    Overflow_In,
    Data_In,
    SupportsGetItem,
    SupportsLength,
    SupportsLengthGetItem,
)
from typing import Any, Callable, Mapping, Sequence, Optional, Union, overload
from typing_extensions import ParamSpec, TypeVar, Concatenate


_TargetT = TypeVar('_TargetT')
_TargetP = ParamSpec('_TargetP')
_DataT = TypeVar('_DataT')
TargetFunction = Callable[Concatenate[_DataT, _TargetP], _TargetT]
Dataset = Union[
    SupportsLengthGetItem[_DataT], SupportsGetItem[_DataT], SupportsLength, Any
]


NoParamReturn = Callable[
    Concatenate[Dataset[_DataT], _TargetP],
    ConcurrentProcessing[_TargetP, _TargetT, _DataT],
]
WithParamReturn = Callable[
    [TargetFunction[_DataT, _TargetP, _TargetT]],
    NoParamReturn[_DataT, _TargetP, _TargetT],
]
FullParamReturn = Callable[
    Concatenate[Dataset[_DataT], _TargetP],
    ConcurrentProcessing[_TargetP, _TargetT, _DataT],
]


@overload
def processor(
    __function: TargetFunction[_DataT, _TargetP, _TargetT],
) -> NoParamReturn[_DataT, _TargetP, _TargetT]: ...


@overload
def processor(
    *,
    args: Sequence[Data_In] = (),
    kwargs: Mapping[str, Data_In] = {},
    ignore_errors: Sequence[type[Exception]] = (),
    suppress_errors: bool = False,
    **overflow_kwargs: Overflow_In,
) -> WithParamReturn[_DataT, _TargetP, _TargetT]: ...


@overload
def processor(
    __function: TargetFunction[_DataT, _TargetP, _TargetT],
    *,
    args: Sequence[Data_In] = (),
    kwargs: Mapping[str, Data_In] = {},
    ignore_errors: Sequence[type[Exception]] = (),
    suppress_errors: bool = False,
    **overflow_kwargs: Overflow_In,
) -> FullParamReturn[_DataT, _TargetP, _TargetT]: ...


def processor(
    __function: Optional[TargetFunction[_DataT, _TargetP, _TargetT]] = None,
    *,
    args: Sequence[Data_In] = (),
    kwargs: Mapping[str, Data_In] = {},
    ignore_errors: Sequence[type[Exception]] = (),
    suppress_errors: bool = False,
    **overflow_kwargs: Overflow_In,
) -> Union[
    NoParamReturn[_DataT, _TargetP, _TargetT],
    WithParamReturn[_DataT, _TargetP, _TargetT],
    FullParamReturn[_DataT, _TargetP, _TargetT],
]:
    """
    Decorate a function to run it in a thread

    Parameters
    ----------
    :param __function: The function to run in a thread
    :param args: Keyword-Only arguments to pass into `thread.Thread`
    :param kwargs: Keyword-Only keyword arguments to pass into `thread.Thread`
    :param ignore_errors: Keyword-Only arguments to pass into `thread.Thread`
    :param suppress_errors: Keyword-Only arguments to pass into `thread.Thread`
    :param **: Keyword-Only arguments to pass into `thread.Thread`

    Returns
    -------
    :return decorator:

    Use Case
    --------
    Now whenever `myfunction` is invoked, it will be executed in a thread and the `Thread` object will be returned

    >>> @thread.threaded
    >>>   def myfunction(*args, **kwargs): ...

    >>> myJob = myfunction(1, 2)
    >>> type(myjob)
    > Thread

    You can also pass keyword arguments to change the thread behaviour, it otherwise follows the defaults of `thread.Thread`
    >>> @thread.threaded(daemon = True)
    >>> def myfunction(): ...

    Args will be ordered infront of function-parsed args parsed into `thread.Thread.args`
    >>> @thread.threaded(args = (1))
    >>> def myfunction(*args):
    >>>   print(args)
    >>>
    >>> myfunction(4, 6).get_return_value()
    1, 4, 6
    """

    if not callable(__function):

        def wrapper(
            func: TargetFunction[_DataT, _TargetP, _TargetT],
        ) -> FullParamReturn[_DataT, _TargetP, _TargetT]:
            return processor(
                func,
                args=args,
                kwargs=kwargs,
                ignore_errors=ignore_errors,
                suppress_errors=suppress_errors,
                **overflow_kwargs,
            )

        return wrapper

    overflow_kwargs.update(
        {'ignore_errors': ignore_errors, 'suppress_errors': suppress_errors}
    )

    kwargs = dict(kwargs)

    @wraps(__function)
    def wrapped(
        data: Dataset[_DataT],
        *parsed_args: _TargetP.args,
        **parsed_kwargs: _TargetP.kwargs,
    ) -> ConcurrentProcessing[_TargetP, _TargetT, _DataT]:
        kwargs.update(parsed_kwargs)

        processed_args = (*args, *parsed_args)
        processed_kwargs = {
            i: v for i, v in kwargs.items() if i not in ['args', 'kwargs']
        }

        job = ConcurrentProcessing(
            function=__function,
            dataset=data,
            args=processed_args,
            kwargs=processed_kwargs,
            **overflow_kwargs,
        )
        job.start()
        return job

    return wrapped
