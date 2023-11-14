# Exceptions

> [!NOTE]
> Exceptions from Python's `threading` module are not included

<br />
<details>
  <summary>Jump to</summary>
  <ul>
    <li><a href='#ignoring-exceptions'> Ignoring Exceptions</a></li>
    <li><a href='#exceptions-1'> Exceptions </a></li>
  </ul>
</details>


Don't have the thread library? [See here](./getting-started.md) for installing thread

---

## Ignoring exceptions

When initializing a thread, you can parse a [**suppress_errors**](./threading.md#parameters) bool.<br />
By default it is false, but if set to true, exceptions will not be propagated but just stored within `Thread._errors`

When initializing a thread, you can parse a [**ignore_errors**](./threading.md#parameters) sequence.<br />
By default it is an empty tuple.<br />
Ignored errors will not be propagated and not stored within `Thread._errors`

<br />

### Example
```py
from thread import Thread

def bad_function():
  raise RuntimeError('>:cc')


# Normal behaviour
thread0 = Thread(
  target = bad_function
)
thread0.start()
thread0.join()
# exit(1) RuntimeError(':<<')


# Suppress exceptions
thread1 = Thread(
  target = bad_function,
  suppress_errors = True
)
thread1.start()
thread1.join()
print(thread1._errors) # list[RuntimeError('>:cc')]


# Ignore error
thread2 = Thread(
  target = bad_function,
  ignore_errors = [RuntimeError]
)
thread2.start()
thread2.join()
print(thread2._errors) # list[]


# Non-ignored error
thread3 = Thread(
  target = bad_function,
  ignore_errors = [ValueError]
)
thread3.start()
thread3.join()
# exit(1) RuntimeError(':<<')


# Non-ignored error with suppressing
thread4 = Thread(
  target = bad_function,
  ignore_errors = [ValueError],
  suppress_errors = True
)
thread4.start()
thread4.join()
print(thread4._errors) # list[RuntimeError(':<<')]


# Ignored error with suppressing
thread5 = Thread(
  target = bad_function,
  ignore_errors = [RuntimeError],
  suppress_errors = True
)
thread5.start()
thread5.join()
print(thread5._errors) # list[]
```

<br />


## Exceptions

The list of exceptions that can be thrown

<br />


### ThreadErrorBase

This is the base exception class that all exceptions inherit from

<br />


### ThreadStillRunningError

This is raised when you attempt to invoke a method which requries the thread to not be running, but is running.
> You can wait for the thread to terminate with [**Thread.join()**](./threading.md#methods) before invoking the method

> You can check if the thread is running with [**Thread.is_alive()**](threading.md#methods) before invoking the method

<br />


### ThreadNotRunningError

This is raised when you attempt to invoke a method which requires the thread to be running, but isn't
> You can run the thread with [**Thread.start()**](threading.md#methods) before invoking the method

<br />


### ThreadNotInitializedError

This is raised when you attempt to invoke a method which requires the thread to be initialized, but isn't
> You can initialize and start the thread with [**Thread.start()**](threading.md#methods) before invoking the method

<br />


### HookRuntimeError

This is raised when hooks raise an exception<br />
Conforms to when thread is ran with errors suppressed or ignored

Example traceback
```text
HookRuntimeError: Encountered runtime errors in hooks

1. my_function
>>>>>>>>>>
/usr/home/proj/main.py:50
ZeroDivisionError:
<<<<<<<<<<

2. my_otherfunction
>>>>>>>>>>
ImportError:
<<<<<<<<<<
```

<br />

[See here](./threading.md) for how to using the `thread.Thread` class!
