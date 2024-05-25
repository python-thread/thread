"""
## Thread Exceptions
"""

import traceback
from typing import Any, Optional, Sequence, Tuple


class ErrorBase(Exception):
    """Base exception class for all errors within this library"""

    message: str = 'Something went wrong!'

    def __init__(
        self, message: Optional[str] = None, *args: Any, **kwargs: Any
    ) -> None:
        message = message or self.message
        super().__init__(message, *args, **kwargs)


# THREAD ERRORS #
class ThreadStillRunningError(ErrorBase):
    """Exception class for attempting to invoke a method which requires the thread not be running, but isn't"""

    message: str = 'Thread is still running, unable to invoke method. You can wait for the thread to terminate with `Thread.join()` or check with `Thread.is_alive()`'


class ThreadNotRunningError(ErrorBase):
    """Exception class for attempting to invoke a method which requires the thread to be running, but isn't"""

    message: str = (
        'Thread is not running, unable to invoke method. Have you ran `Thread.start()`?'
    )


class ThreadNotInitializedError(ErrorBase):
    """Exception class for attempting to invoke a method which requires the thread to be initialized, but isn't"""

    message: str = 'Thread is not initialized, unable to invoke method.'


class HookRuntimeError(ErrorBase):
    """Exception class for hook runtime errors"""

    message: str = 'Encountered runtime errors in hooks'
    count: int = 0

    def __init__(
        self, message: Optional[str] = '', extra: Sequence[Tuple[Exception, str]] = []
    ) -> None:
        """
        Extra for parsing all hooks that errored

        Parameters
        ----------
        :param message: The message to be parsed, can be left blank
        :param extra: Tuple of (Exception_Raised, function_name)
        """
        new_message: str = message or self.message

        for i, v in enumerate(extra):
            trace = '\n'.join(traceback.format_stack())
            new_message += f'\n\n{i}. {v[1]}\n>>>>>>>>>>'
            new_message += f'{trace}\n{v[0]}'
            new_message += '<<<<<<<<<<'
            super().__init__(new_message)
