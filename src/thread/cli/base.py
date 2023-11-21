import os
import time
import json
import typer
import inspect
import importlib

import logging
from typing import Union, Pattern, Required, Optional, Callable

from . import __version__
from .utils import DebugOption, VerboseOption, QuietOption, verbose_args_processor, kwargs_processor
logger = logging.getLogger('base')


cli_base = typer.Typer(
  no_args_is_help = True,
  context_settings = {
    'help_option_names': ['-h', '--help']
  }
)


def version_callback(value: bool):
  if value:
    typer.echo(f'v{__version__}')
    raise typer.Exit()


@cli_base.callback(invoke_without_command = True)
def callback(
  version: bool = typer.Option(
    None, '--version',
    callback = version_callback,
    help = 'Get the current installed version',
    is_eager = True
  ),

  debug: bool = DebugOption,
  verbose: bool = VerboseOption,
  quiet: bool = QuietOption
):
  """Thread CLI"""
  verbose_args_processor(debug, verbose, quiet)



@cli_base.command(context_settings = {'allow_extra_args': True})
def process(
  ctx: typer.Context,
  func: str = typer.Argument(help = '(path.to.file:function_name) OR (lambda x: x)'),
  dataset: str = typer.Argument(help = '(path/to/file.txt) OR ([ i for i in range(2) ])'),

  args: list[str] = typer.Option([], '--args', '-a', help = 'Arguments passed to each thread'),
  threads: int = typer.Option(8, '--threads', '-t', help = 'Maximum number of threads (will scale down based on dataset size)'),

  daemon: bool = typer.Option(False, '--daemon', '-d', help = 'Threads to run in daemon mode'),
  
  debug: bool = DebugOption,
  verbose: bool = VerboseOption,
  quiet: bool = QuietOption
):
  """
  Execute parallel processing\n
  Kwargs can be parsed by adding overflow arguments in pairs\n
  $ thread process ... k1 v1 k2 v2\n
  => kwargs = {k1: v1, k2: v2}\n\n

  Single kwargs will be ignored\n
  $ thread process ... a1\n
  => kwargs = {}
  """
  verbose_args_processor(debug, verbose, quiet)
  kwargs = kwargs_processor(ctx)
  logger.debug('Processed kwargs: %s' % kwargs)


  # Loading function
  f = None
  try:
    logger.info('Attempted to interpret function')
    f = eval(func) # I know eval is bad practice, but I have yet to find a safer replacement
    logger.debug(f'Evaluated function: %s' % f)

    if not inspect.isfunction(f):
      logger.info('Invalid function')
  except Exception:
    logger.info('Failed to interpret function')

  if not f:
    try:
      logger.info('Attempting to fetch function file')

      fPath, fName = func.split(':')
      f = importlib.import_module(fPath).__dict__[fName]
      logger.debug(f'Evaluated function: %s' % f)

      if not inspect.isfunction(f):
        logger.info('Not a function')
        raise Exception('Not a function')
    except Exception as e:
      logger.warning('Failed to fetch function')
      raise typer.BadParameter('Failed to fetch function') from e
    



  # Loading dataset
  ds: Union[list, tuple, set, None] = None
  try:
    logger.info('Attempting to interpret dataset')
    ds = json.loads(dataset)
    logger.debug(f'Evaluated dataset: %s' % ds)

    if not isinstance(ds, (list, tuple, set)):
      logger.info('Invalid dataset literal')
      ds = None
  
  except Exception:
    logger.info('Failed to interpret dataset')

  if not ds:
    try:
      logger.info('Attempting to fetch data file')
      if not os.path.isfile(dataset):
        logger.info('Invalid file path')
        raise Exception('Invalid file path')

      with open(dataset, 'r') as a:
        ds = [ i.endswith('\n') and i[:-2] for i in a.readlines() ]
    except Exception as e:
      logger.warning('Failed to read dataset')
      raise typer.BadParameter('Failed to read dataset') from e
    
  logger.info('Interpreted dataset')


  # Setup
  logger.debug('Importing module')
  from ..thread import ParallelProcessing
  logger.info('Spawning threads... [Expected: {tcount} threads]'.format(tcount=min(len(ds), threads)))

  newProcess = ParallelProcessing(
    function = f,
    dataset = list(ds),
    args = args,
    kwargs = kwargs,
    daemon = daemon,
    max_threads = threads
  )

  logger.info('Created parallel process')
  logger.info('Starting parallel process')

  start_t = time.perf_counter()
  newProcess.start()

  logger.info('Started parallel process')
  logger.info('Waiting for parallel process to complete, this may take a while...')

  result = newProcess.get_return_values()

  logger.info(f'Completed in {(time.perf_counter() - start_t):.5f}s')
  typer.echo(result)
