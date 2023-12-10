"""
Import and config CLI commands
"""

__version__ = '0.1.3'
from ..utils.logging_config import logging, ColorLogger
logging.setLoggerClass(ColorLogger)


# Import #
from .base import cli_base as app
from .process import process as process_cli

app.command(
  name = 'process',
  no_args_is_help = True,
  context_settings = {'allow_extra_args': True}
)(process_cli)
