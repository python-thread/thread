"""Parallel Processing command"""

import os
import time
import json
import inspect
import importlib

import typer
import logging
from typing import Union

from rich.progress import Progress, TextColumn, BarColumn, TimeRemainingColumn, TimeElapsedColumn
from .utils import DebugOption, VerboseOption, QuietOption, verbose_args_processor, kwargs_processor

logger = logging.getLogger('base')


def process(
  func: str = typer.Argument(help = '[blue].path.to.file[/blue]:[blue]function_name[/blue] OR [blue]lambda x: x[/blue]'),
  dataset: str = typer.Argument(help = '[blue]./path/to/file.txt[/blue] OR [blue][ i for i in range(2) ][/blue]'),

  args: list[str] = typer.Option([], '--arg', '-a', help = '[blue]Arguments[/blue] passed to each thread'),
  kargs: list[str] = typer.Option([], '--kwarg', '-kw', help = '[blue]Key-Value arguments[/blue] passed to each thread'),
  threads: int = typer.Option(8, '--threads', '-t', help = 'Maximum number of [blue]threads[/blue] (will scale down based on dataset size)'),

  daemon: bool = typer.Option(False, '--daemon', '-d', help = 'Threads to run in [blue]daemon[/blue] mode'),
  graceful_exit: bool = typer.Option(True, '--graceful-exit', '-ge', is_flag = True, help = 'Whether to [blue]gracefully exit[/blue] on abrupt exit (etc. CTRL+C)'),
  output: str = typer.Option('./output.json', '--output', '-o', help = '[blue]Output[/blue] file location'),
  fileout: bool = typer.Option(True, '--fileout', is_flag = True, help = 'Whether to [blue]write[/blue] output to a file'),
  stdout: bool = typer.Option(False, '--stdout', is_flag = True, help = 'Whether to [blue]print[/blue] the output'),
  
  debug: bool = DebugOption,
  verbose: bool = VerboseOption,
  quiet: bool = QuietOption
):
  """
  [bold]Utilise parallel processing on a dataset[/bold]
  
  \b\n
  [bold white]:glowing_star: Important[/bold white]
  Args and Kwargs can be parsed by adding multiple -a or -kw

  [green]$ thread[/green] [blue]process[/blue] ... -a 'an arg' -kw myKey=myValue -arg testing --kwarg a1=a2
  [white]=> args = [ [green]'an arg'[/green], [green]'testing'[/green] ][/white]
  [white]   kwargs = { [green]'myKey'[/green]: [green]'myValue'[/green], [green]'a1'[/green]: [green]'a2'[/green] }[/white]
  
  [blue][u]                                 [/u][/blue]

  Learn more from our [link=https://github.com/caffeine-addictt/thread/blob/main/docs/command-line.md#parallel-processing-thread-process]documentation![/link]
  """
  verbose_args_processor(debug, verbose, quiet)
  kwargs = kwargs_processor(kargs)
  logger.debug('Processed kwargs: %s' % kwargs)


  # Verify output
  if not fileout and not stdout:
    raise typer.BadParameter('No output method specified')
  
  if fileout and not os.path.exists('/'.join(output.split('/')[:-1])):
    raise typer.BadParameter('Output file directory does not exist')




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
    ds = eval(dataset)
    logger.debug(f'Evaluated dataset: %s' % (str(ds)[:125] + '...' if len(str(ds)) > 125 else ds))

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
  from ..thread import Settings, ParallelProcessing
  logger.info('Spawning threads... [Expected: {tcount} threads]'.format(tcount=min(len(ds), threads)))

  Settings.set_graceful_exit(graceful_exit)
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

  typer.echo('Started parallel process')
  typer.echo('Waiting for parallel process to complete, this may take a while...')

  with Progress(
    TextColumn('[bold blue]{task.description}', justify = 'right'),
    BarColumn(bar_width = None),
    '[progress.percentage]{task.percentage:>3.1f}%',
    '•',
    TimeRemainingColumn(),
    '•',
    TimeElapsedColumn()
  ) as progress:
    percentage = 0
    job = progress.add_task('Working...', total = 100)

    while percentage < 100:
      percentage = round(sum(i.progress for i in newProcess._threads) / (len(newProcess._threads) or 8), 2) * 100
      progress.update(job, completed = percentage)
      time.sleep(0.1)

  result = newProcess.get_return_values()

  typer.echo(f'Completed in {(time.perf_counter() - start_t):.5f}s')
  if fileout:
    typer.echo(f'Writing file to {output}...')
    try:
      with open(output, 'w') as f:
        json.dump(result, f, indent = 2)
      typer.echo(f'Wrote to file')
    except Exception as e:
      logger.error('Failed to write to file')
      logger.debug(str(e))

  if stdout:
    typer.echo(result)
