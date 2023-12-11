# Code Style
The following is a general guide on how to style your work so that the project
remains consistent throughout all files. Please read this document in it's entirety
and refer to it throughout the development of your contribution.


## Commit Message Guidelines
When committing, commit messages are prefixed with a `+` or `-`. Depending on the type of change made influences which prefix is used.

 - `+` when something is added.
 - `-` when something is removed.
 - none: when neither is applicable, like merge commits.

Commit messages are also to begin with an uppercase character. Below list some example commit messages.

```
git commit -m "+ Added README.md"
git commit -m "- Removed README.md"
git commit -m "Moved README.md"
```


## General Guidelines
```python
class ExampleClass:
  """
  ExampleClass
  ------------
  Example class for CODESTYLE.md
  """

  _private_attribute : int # Desired type here
  public_attribute   : int

  def __init__(
    self,
    public_attribute: int
  ) -> None: # note the result
    """
    Initializes a ExampleClass

    Parameters
    ----------
    :param public_attribute: example attribute
    """
    self.public_attribute = public_attribute
    self.private_attribute = square(public_attribute)

  def square(self, value: int) -> int:
    """
    Square roots a value

    Parameters
    ----------
    :param value: value that you want squared
    """
    return value**2
```

