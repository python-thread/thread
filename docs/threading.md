# Thread Class Documentation

I will lay out how to use the `thread.Thread` class!

<br />
<details>
  <summary>Jump to</summary>
  <ul>
    <li><a href='#importing-the-class'> Import the class</a></li>
    <li><a href='#initializing-a-thread'> Initialize a thread </a></li>
    <li><a href='#parameters'> Parameters </a></li>
    <li><a href='#attributes'> Attributes </a></li>
    <li><a href='#methods'> Class Methods </a></li>
    <li><a href='#behviours'> Behaviours </a></li>
  </ul>
</details>


Don't have the thread library? [See here](./getting-started.md) for installing thread

---

## Importing the class

```py
from thread import Thread
```

<br />


## Initializing a thread

A simple thread can be prepared to be initialized with this
```py
def my_target(): ...

# Reccommended way
my_thread = Thread(
  target = my_target
)

# OR
# Not the reccommended way
my_thread = Thread(my_target)
```

A thread can be ran by invoking the `start()` method
```py
my_thread.start()
```

<br />


### Parameters

* target : (Data_In, *args, **kwargs) -> Any | Data_Out
  > This should be a function that takes in anything and returns anything

* args : Sequence[Data_In] = ()
  > This should be an interable sequence of arguments parsed to the `target` function <br />
  > (e.g. tuple('foo', 'bar'))
  
* kwargs : Mapping[str, Data_In] = {}
  > This should be the kwargs pased to the `target` function<br />
  > (e.g. dict(foo = 'bar'))

* ignore_errors : Sequence[type[Exception]] = ()
  > This should be an interable sequence of all exceptions to ignore.<br />
  > To ignore all exceptions, parse tuple(Exception)

* suppress_errors : bool = False
  > This should be a boolean indicating whether exceptions will be raised.<br />
  > If true, exceptions will only write to internal `errors` property<br />
  > If false, exceptions will propagate if not ignored

* name : Optional[str] = None
  > This is an argument parsed to `threading.Thread`

* daemon : bool = False
  > This is an argument parsed to `threading.Thread`

* group : None = None
  > This is an argument parsed to `threading.Thread`<br />
  > [!NOTE]<br />
  > This does nothing

* *overflow_args : Overflow_In
  > These are arguments parsed to `threading.Thread`

* **overflow_kwargs : Overflow_In
  > These are arguments parsed to `threading.Thread`

<br />


### Attributes

These are attributes of [`Thread`](#importing-the-class) class

* result : Data_Out
  > The result value of the thread
  > **Raises** [`ThreadNotInitializedError`](./exceptions.md#threadNotInitializedError)<br />
  > **Raises** [`ThreadNotRunningError`](./exceptions.md#threadnotrunningerror)<br />
  > **Raises** [`ThreadStillRunningError`](./exceptions.md#threadStillRunningError)

* status : str
  > The current status of the thread

<br />


### Methods

These are methods of [`Thread`](#importing-the-class) class

* start : () -> None
  > Initializes the thread and starts it<br />
  > **Raises** [`ThreadStillRunningError`](./exceptions.md#threadStillRunningError)

* is_alive : () -> bool
  > Indicates whether the thread is still alive<br />
  > **Raises** [`ThreadNotInitializedError`](./exceptions.md#threadNotInitializedError)

* add_hook : ((Data_Out) -> Any | None) -> None
  > Hooks will be automatically invoked after a thread successfully completes, parsing the return value as the first argument<br />
  > **Raises** [`ThreadNotInitializedError`](./exceptions.md#threadNotInitializedError)<br />
  > **Raises** [`ThreadNotRunningError`](./exceptions.md#threadnotrunningerror)

* get_return_value : () -> Data_Out
  > Halts the current thread execution until the thread completes

* join : () -> JoinTerminatedStatus
  > Halts the current thread execution until a thread completes or exceeds the timeout<br />
  > **Raises** [`ThreadNotInitializedError`](./exceptions.md#threadNotInitializedError)<br />
  > **Raises** [`ThreadNotRunningError`](./exceptions.md#threadnotrunningerror)

* kill : (yielding: bool = False, timeout: float = 5) -> bool
  > Schedules the thread to be killed<br />
  > If yielding is True, it halts the current thread execution until the thread is killed or the timeout is exceeded<br />
  > **Raises** [`ThreadNotInitializedError`](./exceptions.md#threadnotinitializederror)<br />
  > **Raises** [`ThreadNotRunningError`](./exceptions.md#threadnotrunningerror)<br />
  > [!NOTE]<br />
  > This only schedules the thread to be killed, and does not immediately kill the thread

<br />


## Behviours

These are a list of thread behvaiours

### Killing Threads - Introduced in v0.1.2

While preferably not utilized, we do support killing threads.<br />
We mark a thread to be killed, and will only be killed when the thread invokes `sys.settrace()`.

> [!IMPORTANT]<br />
> This means that if your `target` has a long `time.wait()` call, it will only be killed after it moves onto the next line.

<br />

Want an alternative? Learn about [Daemonized Threads!](https://www.geeksforgeeks.org/python-daemon-threads/)

<br />


### Gracefull Exiting - Introduced in v0.1.2

When the program is abruptly stopped with `CTRL+C` for example, active threads will now attempt to gracefully kill itself.<br />

This is not to be an "end-all be-all" for managing threads. You should still try to properly exit a thread before abruptly exiting the program, or utilize a `Daemonized Thread`.

<br />


Now you know how to use the [`Thread`](#importing-the-class) class!

[See here](./parallel-processing.md) for how to using the `thread.ParallelProcessing` class!
