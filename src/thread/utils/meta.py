import sys

# compatibility for python <3.10
if sys.version_info < (3, 10):
    import importlib_metadata as metadata
else:
    from importlib import metadata

__all__ = ['metadata']
