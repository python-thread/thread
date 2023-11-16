import traceback
from typing import Any, Optional


class ThreadErrorBase(Exception):
  """Base exception class for all errors within this library"""
  message: str = 'Something went wrong!'
  def __init__(self, message: Optional[str] = None, *args: Any, **kwargs: Any) -> None:
    message = message or self.message
    super().__init__(message, *args, **kwargs)


class ThreadStillRunningError(ThreadErrorBase):
  """Exception class for attempting to invoke a method which requries the thread not be running, but isn't"""
  message: str = 'Thread is still running, unable to invoke method. You can wait for the thread to terminate with `Thread.join()` or check with `Thread.is_alive()`'

class ThreadNotRunningError(ThreadErrorBase):
  """Exception class for attempting to invoke a method which requires the thread to be running, but isn't"""
  message: str = 'Thread is not running, unable to invoke method. Have you ran `Thread.start()`?'

class ThreadNotInitializedError(ThreadErrorBase):
  """Exception class for attempting to invoke a method which requires the thread to be initialized, but isn't"""
  message: str = 'Thread is not initialized, unable to invoke method.'

class HookRuntimeError(ThreadErrorBase):
  """Exception class for hook runtime errors"""
  message: str = 'Encountered runtime errors in hooks'
  count: int = 0

  def add_exception_case(self, func_name: str, error: Exception):
    self.count += 1
    trace = '\n'.join(traceback.format_stack())

    self.add_note(f'\n{self.count}. {func_name}\n>>>>>>>>>>')
    self.add_note(f'{trace}\n{error}')
    self.add_note('<<<<<<<<<<')
