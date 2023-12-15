"""
## Decorators

Documentation: https://thread.ngjx.org
"""

from functools import wraps
from abc import ABC, abstractmethod

from ._types import TargetFunction, Overflow_In, Data_Out, Data_In
from typing import Any, Callable, Mapping, Tuple

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
    """init"""
    self.args = args
    self.kwargs = kwargs

  def __call__(self, *args: Any, **kwargs: Any) -> Data_Out:
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
    if callable(self.args[0]) and self.__validate__(args, kwargs):
      func = self.args[0]
      return self.__execute__(func, args, kwargs)
    
    elif not callable(self.args[0]):
      func = args[0]

      @wraps(self.__execute__)
      def wrapper(*args, **kwargs):
        if self.__validate__(args, kwargs):
          return self.__execute__(func, args, kwargs)
      return wrapper
    
    else:
      raise ArgumentValidationError()


  @abstractmethod
  def __execute__(self, func: Callable[..., Data_Out], args: Tuple[Any, ...], kwargs: Mapping[str, Any]) -> Data_Out:
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

