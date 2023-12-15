"""
## Decorators

Documentation: https://thread.ngjx.org
"""

import inspect
from functools import wraps
from abc import ABC, abstractmethod

from ._types import TargetFunction, Overflow_In, Data_Out, Data_In
from typing import Any, Callable, Mapping, Tuple, Sequence, Optional, Union

from .thread import Thread
from .exceptions import AbstractInvokationError, ArgumentValidationError


class DecoratorBase(ABC):
  """
  Decorator Base Class

  This should only be used from inheriting classes

  Use Case
  --------
  ```py
  class MyDecorator(DecoratorBase):
    # DocString here for decorator without arguments
    
    # Arguments to the decorator are here
    args: Tuple[Any, ...]
    kwargs: Mapping[str, Any]

    def __init__(self, *args, **kwargs):
      # DocString here for decorator with arguments
      # If you want to have type hinting
      # If you want to validate arguments to decorator
      super().__init__(*args, **kwargs)

    def __call__(self, *args, **kwargs):
      return super().__call__(*args, **kwargs)

    def __validate__(self, args, kwargs):
      # If you want to validate arguments to the wrapped function
      return bool

    def __execute__(self, func, args, kwargs):
      return func(*args, **kwargs)
  ```
  """

  args: Tuple[Any, ...]
  kwargs: Mapping[str, Any]

  def __init__(self, *args: Any, **kwargs: Any) -> None:
    """
    Decorator Arguments

    There arguments will `NOT` be parsed to the wrapped function

    Parameters
    ----------
    :param *: Positional arguments
    :param **: Keyword arguments
    """
    self.args = args
    self.kwargs = kwargs

  def __call__(self, *args: Any, **kwargs: Any) -> Union[Any, Callable[..., Any]]:
    """
    The main logic to allow decorators to be invoked:

    ```py
    @MyDecorator
    def a(): ...

    @MyDecorator()
    def b(): ...

    @MyDecorator(1, 2, 3)
    def c(): ...
    ```
    """
    is_callable = (len(self.args) >= 1) and callable(self.args[0])
    if is_callable and self.__validate__(args, kwargs):
      func = self.args[0]
      return self.__execute__(func, args, kwargs)
    
    elif not is_callable:
      func = args[0]

      @wraps(self.__execute__)
      def wrapper(*args, **kwargs):
        if self.__validate__(args, kwargs):
          return self.__execute__(func, args, kwargs)
        else:
          raise ArgumentValidationError()
      return wrapper
    
    else:
      raise ArgumentValidationError()


  @abstractmethod
  def __execute__(self, func: Callable[..., Data_Out], args: Tuple[Any, ...], kwargs: Mapping[str, Any]):
    """
    The main code returning the result of the wrapped method

    Parameters
    ----------
    :param func: The wrapped function
    :param args: The tuple of parsed arguments
    :param kwargs: The tuple of parsed keyword arguments

    Returns
    -------
    :returns Data_Out: The result of the wrapped function

    Raises
    ------
    AbstractInvocationsError: When the base class abstract method is invoked

    Use Case
    --------
    ```py
    class MyDecorator(DecoratorBase):
      ...
      def __execute__(self, func, args, kwargs):
        return func(*args, **kwargs)
    ```
    """
    raise AbstractInvokationError('__execute__')

  @abstractmethod
  def __validate__(self, args: Tuple[Any, ...], kwargs: Mapping[str, Any]) -> bool:
    """
    Validate arguments parsed to the wrapped method

    Parameters
    ----------
    :param args: Tuple of parsed positional arguments
    :param kwargs: Dictionary of parsed keyword arguments

    Returns
    -------
    :returns bool: True if the arguments are valid

    Raises
    ------
    AbstractInvokationError: When the base class abstract method is invoked

    Use Case
    --------
    ```py
    @MyDecorator
    def myfunction(*args, **kwargs): ...

    myfunction(1, 2, 3) # Arguments parsed here is validated here
    ```
    """
    raise AbstractInvokationError('__validate__')




class threaded(DecoratorBase):
  """
  Decorate a function to run it in a thread

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
  >>> def myotherfunction(): ...
  """

  def __init__(
    self,
    func: Optional[TargetFunction] = None,
    *,
    args: Sequence[Data_In] = (),
    kwargs: Mapping[str, Data_In] = {},
    ignore_errors: Sequence[type[Exception]] = (),
    suppress_errors: bool = False,
    **overflow_kwargs: Overflow_In
  ) -> None:
    """
    Decorate a function to ru nit in a thread

    Parameters
    :param func: Automatically passed in
    :param args: 
    """

    compiled: Mapping[str, Any] = dict(
      args = args,
      kwargs = kwargs,
      ignore_errors = ignore_errors,
      suppress_errors = suppress_errors,
      **overflow_kwargs
    )

    # Validate arguments
    allowed_params = inspect.signature(Thread.__init__).parameters
    for key in compiled:
      if key not in allowed_params:
        raise ArgumentValidationError(f'{key} is not a keyword argument for thread.Thread')
    super().__init__(**compiled) if func is None else super().__init__(func, **compiled)


  def __call__(
    self,
    func: Optional[TargetFunction] = None,
    *args: Any,
    **kwargs: Any
  ) -> Any:
    if func is not None:
      args = (func, *args)
    return super().__call__(*args, **kwargs)


  def __validate__(self, *args, **kwargs) -> bool:
    return True
  
  
  def __execute__(self, func: TargetFunction, args: Tuple[Any, ...], kwargs: dict[str, Any]) -> Thread:
    # Join parsed args and kwargs with decorator defined args and kwargs
    parsedKwargs = {}
    for i, v in self.kwargs.items():
      if i == 'args':     args = ( *v, *args)
      elif i == 'kwargs': kwargs[i] = v
      else:               parsedKwargs[i] = v

    job = Thread(
      target = func,
      args = args,
      kwargs = kwargs,
      *self.args,
      **parsedKwargs
    )
    job.start()
    return job
