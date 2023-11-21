"""
Import and config CLI commands
"""

__version__ = '0.1.2'
from ..config import logging, ColorLogger
logging.setLoggerClass(ColorLogger)


# Import #
from .base import cli_base as app
