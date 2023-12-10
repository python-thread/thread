# Thread Configuration Documentation

I will lay out the configuration options!

<br />
<details>
  <summary>Jump to</summary>
  <ul>
    <li><a href='#importing-the-class'> Import the class </a></li>
    <li><a href='#graceful-exiting'> Graceful Exit </a></li>
  </ul>
</details>


Don't have the thread library? [See here](./getting-started.md) for installing thread

---

## Importing the class

```py
from thread import Thread
```

<br />


## Graceful Exiting

```py
from thread import Settings

# Enable/Disable graceful exiting
Settings.set_graceful_exit(True)
Settings.set_graceful_exit(False)
```

<br />


Now you know the configuration options available!

[See here](./parallel-processing.md) for how to using the `thread.ParallelProcessing` class!
