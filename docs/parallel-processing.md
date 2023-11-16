# Parallel Processing Documentation

I will lay out how to use the `thread.ParallelProcessing` class!

<br />
<details>
  <summary>Jump to</summary>
  <ul>
    <li><a href='#how-does-it-work'> How it works </a></li>
    <li><a href='#initializing-a-parallel-process'> Initialize a Parallel Process </a></li>
    <li><a href='#parameters'> Parameters </a></li>
    <li><a href='#attributes'> Attributes </a></li>
    <li><a href='#methods'> Class Methods </a></li>
  </ul>
</details>


Don't have the thread library? [See here](./getting-started.md) for installing thread

---

## Importing the class

```py
from thread import ParallelProcessing
```

<br />


## How does it work?

Parallel Processing works best by optimizing data processing with large datasets.

What it does:
```py
dataset = [1, 2, 3, ..., 2e10]

# Splits into chunks as evenly as possible
# thread_count = min(max_threads, len(dataset))
# n == len(chunks) == len(thread_count)
chunks = [[1, 2, 3, ...], [50, 51, 52, ...], ...]

# Initialize and run n threads
# each thread handles 1 chunk of data and parses it into the function

# processed data is arranged back in order

# processed data is returned as a list[Data_Out]
```

<br />


## Initializing a parallel process

A simple example
```py
def my_data_processor(Data_In) -> Data_Out: ...

# Reccommended way
my_processor = ParallelProcessing(
  function = my_data_processor,
  dataset = [i in range(0, n)]
)

# OR
# Not the reccommended way
my_processor = ParallelProcessing(my_data_processor, [i in range(0, n)])
```

It can be ran by invoking the `start()` method
```py
my_processor.start()
```

> [!NOTE]
> The **threading.ParallelProcessing()** class from python will only be initialized when **start()** is invoked

<br />


### Parameters

* function : (DataProcessor, dataset, *args, **kwargs) -> Any | Data_Out
  > This should be a function that takes in a dataset and/or anything and returns Data_Out and/or anything

* dataset : Sequence[Data_In] = ()
  > This should be an interable sequence of arguments parsed to the `DataProcessor` function<br />
  > (e.g. tuple('foo', 'bar'))
  
* *overflow_args : Overflow_In
  > These are arguments parsed to [**thread.Thread**](./threading.md#parameters)

* **overflow_kwargs : Overflow_In
  > These are arguments parsed to [**thread.Thread**](./threading.md#parameters)<br />
  > [!NOTE]<br />
  > If `args` is present, then it will automatically be removed from kwargs and joined with `overflow_args`

* **Raises** AssertionError: max_threads is invalid

<br />


### Attributes

These are attributes of [`ParallelProcessing`](#importing-the-class) class

* results : List[Data_Out]
  > The result value<br />
  > **Raises** [`ThreadNotInitializedError`](./exceptions.md#threadNotInitializedError)<br />
  > **Raises** [`ThreadNotRunningError`](./exceptions.md#threadnotrunningerror)<br />
  > **Raises** [`ThreadStillRunningError`](./exceptions.md#threadStillRunningError)

<br />


### Methods

These are methods of [`ParallelProcessing`](#importing-the-class) class

* start : () -> None
  > Initializes the threads and starts it<br />
  > **Raises** [`ThreadStillRunningError`](./exceptions.md#threadStillRunningError)

* is_alive : () -> bool
  > Indicates whether the thread is still alive<br />
  > **Raises** [`ThreadNotInitializedError`](./exceptions.md#threadNotInitializedError)

* get_return_values : () -> Data_Out
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


Now you know how to use the [`ParallelProcessing`](#importing-the-class) class!

[See here](./parallel-processing.md) for how to using the `thread.ParallelProcessing` class!
