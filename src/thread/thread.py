import numpy
import threading
from . import exceptions

from functools import wraps
from dataclasses import dataclass
from typing import (
  Any, List,
  Callable, Concatenate,
  Optional, Literal,
  Iterable, Mapping, Sequence
)


@dataclass
class JoinTerminatedStatus:
  """How the `Thread.join()` method terminated"""
  status: Literal['Timeout Exceeded', 'Thread terminated']


ThreadStatus = Literal['Idle', 'Running', 'Invoking hooks', 'Completed', 'Errored']
Data_In = Any; Data_Out = Any
Overflow_In = Any

class Thread:
  """
  Wraps python's `threading.Thread` class
  ---------------------------------------

  Type-Safe and provides more functionality on top
  """

  _thread        : Optional[threading.Thread]
  status         : ThreadStatus
  hooks          : List[Callable[[Data_Out], Any | None]]
  returned_value : Data_Out

  target         : Callable[Concatenate[Data_In, ...], Data_Out]
  args           : Sequence[Data_In]
  kwargs         : Mapping[str, Data_In]

  errors         : List[Exception]
  ignore_errors  : Sequence[Exception]
  suppress_errors: bool

  overflow_args  : Sequence[Overflow_In]
  overflow_kwargs: Mapping[str, Overflow_In]

  def __init__(
    self,
    target: Callable[Concatenate[Data_In, ...], Data_Out],
    args: Sequence[Data_In] = (),
    kwargs: Mapping[str, Data_In] = {},
    ignore_errors: Sequence[Exception] = (),
    suppress_errors: bool = False,

    name: Optional[str] = None,
    daemon: bool = False,
    *overflow_args: Overflow_In, **overflow_kwargs: Overflow_In
  ) -> None:
    """
    Initializes a thread

    Parameters
    ----------
    :param target: This should be a function that takes in anything and returns anything
    :param args: This should be an interable sequence of arguments parsed to the `target` function (e.g. tuple('foo', 'bar'))
    :param kwargs: This should be the kwargs pased to the `target` function (e.g. dict(foo = 'bar'))
    :param ignore_errors: This should be an interable sequence of all exceptions to ignore. To ignore all exceptions, parse tuple(Exception)
    :param suppress_errors: This should be a boolean indicating whether exceptions will be raised, else will only write to internal `errors` property
    :param name: This is an argument parsed to `threading.Thread`
    :param daemon: This is an argument parsed to `threading.Thread`
    :param *: These are arguments parsed to `threading.Thread`
    :param **: These are arguments parsed to `thread.Thread`
    """
    self.status = 'Idle'
    self.hooks = []

    self.target = self._wrap_target(target)
    self.args = args
    self.kwargs = kwargs

    self.errors = []
    self.ignore_errors = ignore_errors
    self.suppress_errors = suppress_errors

    self.overflow_args = overflow_args
    self.overflow_kwargs = {
      'name': name,
      'daemon': daemon,
      **overflow_kwargs
    }


  def _wrap_target(
    self,
    target: Callable[Concatenate[Data_In, ...], Data_Out]
  ) -> Callable[Concatenate[Data_In, ...], Data_Out]:
    @wraps(target)
    def wrapper(*args: Any, **kwargs: Any) -> Any:
      self.status = 'Running'

      try: self.returned_value = target(*args, **kwargs)
      except Exception as e:
        if e not in self.ignore_errors:
          self.status = 'Errored'
          self.errors.append(e)

          if not self.suppress_errors: raise
          else: return
      
      self.status = 'Invoking hooks'
      self._invoke_hooks()
      self.status = 'Completed'
    return wrapper
  

  def _invoke_hooks(self) -> None:
    trace = exceptions.HookRuntimeError()
    for hook in self.hooks:
      try: hook(self.returned_value)
      except Exception as e:
        if not self.suppress_errors and (e not in self.ignore_errors):
          trace.add_exception_case(
            hook.__name__,
            e
          )

    if trace.count > 0:
      self.errors.append(trace)
      if not self.suppress_errors:
        raise trace
    

  @property
  def result(self) -> Data_Out:
    """
    The return value of the thread
    
    Raises
    ------
    ThreadeStillRunningError: If the thread is still running
    """
    if self.status in ['Invoking hooks', 'Completed']:
      return self.returned_value
    else:
      raise exceptions.ThreadStillRunningError()


  def join(self, timeout: Optional[float] = None) -> 'JoinTerminatedStatus':
    """
    Halts the current thread execution until a thread completes or exceeds the timeout

    Parameters
    ----------
    :param timeout: The maximum time allowed to halt the thread

    Returns
    -------
    :returns JoinTerminatedStatus: Why the method stoped halting the thread

    Raises
    ------
    ThreadNotInitializedError: If the thread is not initialized
    ThreadNotRunningError: If the thread is not running
    """
    if not self._thread:
      raise exceptions.ThreadNotInitializedError()
    
    if self.status == 'Idle':
      raise exceptions.ThreadNotRunningError()

    self._thread.join(timeout)
    return JoinTerminatedStatus(self._thread.is_alive() and 'Timeout Exceeded' or 'Thread terminated')
  

  def get_return_value(self) -> Data_Out:
    """
    Halts the current thread execution until the thread completes

    Returns
    -------
    :returns Any: The return value of the target function
    """
    self.join()
    return self.result
  

  def start(self) -> None:
    """
    Starts the thread
    
    Raises
    ------
    ThreadStillRunningError: If there already is a running thread
    """
    if self._thread is not None and self._thread.is_alive():
      raise exceptions.ThreadStillRunningError()

    self._thread = threading.Thread(
      target = self.target,
      args = self.args,
      kwargs = self.kwargs,
      *self.overflow_args,
      **self.overflow_kwargs
    )
    self._thread.start()



class ParallelProcessing:
  """
  Multi-Threaded Parallel Processing
  ---------------------------------------

  Type-Safe and provides more functionality on top
  """

  _threads       : List[Thread]
  _completed     : int
  _return_vales  : Mapping[int, List[Data_Out]]

  status         : ThreadStatus
  function       : Callable[Concatenate[Sequence[Data_In], ...], List[Data_Out]]
  dataset        : Sequence[Data_In]
  max_threads    : int

  overflow_args  : Sequence[Overflow_In]
  overflow_kwargs: Mapping[str, Overflow_In]
  
  def __init__(
    self,
    function: Callable[Concatenate[Data_In, ...], Data_Out],
    dataset: Sequence[Data_In],
    max_threads: int = 8,

    *overflow_args: Overflow_In, **overflow_kwargs: Overflow_In
  ) -> None:
    """
    Initializes a new Multi-Threaded Pool\n
    Best for data processing
    
    Splits a dataset as evenly as it can among the threads and run them in parallel

    Parameters
    ----------
    :param function: This should be the function to validate each data entry in the `dataset`
    :param dataset: This should be an iterable sequence of data entries
    :param max_threads: This should be an integer value of the max threads allowed
    :param *: These are arguments parsed to `threading.Thread` and `Thread`
    :param **: These are arguments parsed to `thread.Thread` and `Thread`

    Raises
    ------
    AssertionError: invalid `max_threads`
    """
    assert 0 <= max_threads, 'Cannot run a thread pool with max threads set to 0'

    self._threads = []
    self._completed = 0

    self.status = 'Idle'
    self.function = self._wrap_function(function)
    self.dataset = dataset
    self.max_threads = max_threads

    self.overflow_args = overflow_args
    self.overflow_kwargs = overflow_kwargs

  def _wrap_function(
    self,
    function: Callable[Concatenate[Data_In, ...], Data_Out]
  ) -> Callable[Concatenate[Sequence[Data_In], ...], List[Data_Out]]:
    @wraps(function)
    def wrapper(data_chunk: Sequence[Data_In], *args: Any, **kwargs: Any) -> List[Data_Out]:
      computed: List[Data_Out] = []
      for data_entry in data_chunk:
        try:
          v = function(data_entry, *args, **kwargs)
          computed.append(v)
        except Exception as e:
          pass

      self._completed += 1
      if self._completed == len(self._threads):
        self.status = 'Completed'

      return computed
    return wrapper


  @property
  def results(self) -> Data_Out:
    """
    The return value of the threads if completed
    
    Raises
    ------
    ThreadeStillRunningError: If the threads are still running
    """
    if self._completed == len(self._threads):
      results: List[Data_Out] = []
      for thread in self._threads:
        results += thread.result
      return results
    else:
      raise exceptions.ThreadStillRunningError()
  
  def get_return_values(self) -> List[Data_Out]:
    """
    Halts the current thread execution until the thread completes

    Returns
    -------
    :returns Any: The return value of the target function
    """
    results: List[Data_Out] = []
    for thread in self._threads:
      thread.join()
      results += thread.result
    return results
  

  def start(self) -> None:
    """
    Starts the threads
    
    Raises
    ------
    ThreadStillRunningError: If there already is a running thread
    """
    if self.status == 'Running':
      raise exceptions.ThreadStillRunningError()
    
    self.status = 'Running'
    max_threads = min(self.max_threads, len(self.dataset))

    for data_chunk in numpy.array_split(self.dataset, max_threads):
      chunk_thread = Thread(
        target = self.function,
        args = data_chunk.tolist(),
        *self.overflow_args,
        **self.overflow_kwargs
      )
      self._threads.append(chunk_thread)
      chunk_thread.start()
