# Getting started with thread

Thanks for using thread! I hope you find it useful for your projects.

Here's to you get started.

---

## Prerequisites

* Python 3.11+

The project is quite heavily type-annotated, and we use `Concatenate[Any, ...]` in some function declarations.
However `Python <=3.10` does not support `...` being the last argument as laid out in [this stack overflow question](https://stackoverflow.com/questions/74893354/is-literal-ellipsis-really-valid-as-paramspec-last-argument).

If possible, I may release a sister version of thread that is compatible with `Python 3.9+` in the future, but for the time being,
support will extend only from Python 3.11+

<br />


## Installing

### From pip (Recommended)
```sh
pip install thread
```

### Building from source (Not Recommended)
```sh
# Clone this repository
git clone https://github.com/caffeine-addictt/thread

# Install dependencies
pip install poetry

# Build the distribution
python3 -m poetry build

# Install the distribution
pip install -e .
```

<br />


## Importing thread

Import thread into your .py file
```py
import thread
```

Now you have successfully installed thread!

[See here](./threading.md) for how to using the `thread.Thread` class!
