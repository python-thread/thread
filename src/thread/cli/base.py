import os
import time
import json
import inspect
import importlib

import typer
import logging
from rich.progress import Progress, TextColumn, BarColumn, TimeRemainingColumn, TimeElapsedColumn
from typing import Union, Pattern, Required, Optional, Callable

from . import __version__
from .utils import DebugOption, VerboseOption, QuietOption, verbose_args_processor, kwargs_processor
logger = logging.getLogger('base')


cli_base = typer.Typer(
  no_args_is_help = True,
  rich_markup_mode = 'rich',
  context_settings = {
    'help_option_names': ['-h', '--help', 'help']
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
  """
  [b]Thread CLI[/b]\b\n
  [white]Use thread from the terminal![/white]

  [blue][u]                                 [/u][/blue]

  Learn more from our [link=https://github.com/caffeine-addictt/thread/blob/main/docs/command-line.md]documentation![/link]
  """
  verbose_args_processor(debug, verbose, quiet)



# Help and Others
@cli_base.command(rich_help_panel = 'Help and Others')
def help():
  """Get [yellow]help[/yellow] from the community. :question:"""
  typer.echo('Feel free to search for or ask questions here!')
  try:
    logger.info('Attempting to open in web browser...')

    import webbrowser
    webbrowser.open(
      'https://github.com/caffeine-addictt/thread/issues',
      new = 2
    )
    typer.echo('Opening in web browser!')

  except Exception as e:
    logger.warn('Failed to open web browser')
    logger.debug(f'{e}')
    typer.echo('https://github.com/caffeine-addictt/thread/issues')



@cli_base.command(rich_help_panel = 'Help and Others')
def docs():
  """View our [yellow]documentation.[/yellow] :book:"""
  typer.echo('Thanks for using Thread, here is our documentation!')
  try:
    logger.info('Attempting to open in web browser...')
    import webbrowser
    webbrowser.open(
      'https://github.com/caffeine-addictt/thread/blob/main/docs/command-line.md',
      new = 2
    )
    typer.echo('Opening in web browser!')

  except Exception as e:
    logger.warn('Failed to open web browser')
    logger.debug(f'{e}')
    typer.echo('https://github.com/caffeine-addictt/thread/blob/main/docs/command-line.md')



@cli_base.command(rich_help_panel = 'Help and Others')
def report():
  """[yellow]Report[/yellow] an issue. :bug:"""
  typer.echo('Sorry you run into an issue, report it here!')
  try:
    logger.info('Attempting to open in web browser...')
    import webbrowser
    webbrowser.open(
      'https://github.com/caffeine-addictt/thread/issues',
      new = 2
    )
    typer.echo('Opening in web browser!')

  except Exception as e:
    logger.warn('Failed to open web browser')
    logger.debug(f'{e}')
    typer.echo('https://github.com/caffeine-addictt/thread/issues')



# Utils and Configs
@cli_base.command(rich_help_panel = 'Utils and Configs')
def config(configuration: str):
  """
  [blue]Configure[/blue] the system. :wrench:
  """
  typer.echo('Coming soon!')



@cli_base.command(context_settings = {'allow_extra_args': True}, no_args_is_help = True)
def process(
  ctx: typer.Context,
  func: str = typer.Argument(help = '(path.to.file:function_name) OR (lambda x: x)'),
  dataset: str = typer.Argument(help = '(path/to/file.txt) OR ([ i for i in range(2) ])'),

  args: list[str] = typer.Option([], '--args', '-a', help = 'Arguments passed to each thread'),
  threads: int = typer.Option(8, '--threads', '-t', help = 'Maximum number of threads (will scale down based on dataset size)'),

  daemon: bool = typer.Option(False, '--daemon', '-d', help = 'Threads to run in daemon mode'),
  output: str = typer.Option('./output.json', '--output', '-o', help = 'Output file location'),
  fileout: bool = typer.Option(True, '--fileout', is_flag = True, help = 'Weather to write output to a file'),
  stdout: bool = typer.Option(False, '--stdout', is_flag = True, help = 'Weather to print the output'),
  
  debug: bool = DebugOption,
  verbose: bool = VerboseOption,
  quiet: bool = QuietOption
):
  """
  [bold]Utilise parallel processing on a dataset[/bold]
  
  \b\n
  [bold]:glowing_star: Examples[/bold]
  Kwargs can be parsed by adding overflow arguments in pairs
      [green]$ thread process ... k1 v1 k2 v2[/green]
      => kwargs = {k1: v1, k2: v2}

  Single kwargs will be ignored
      [green]$ thread process ... a1[/green]
      => kwargs = {}
  
  """
  verbose_args_processor(debug, verbose, quiet)
  kwargs = kwargs_processor(ctx)
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
