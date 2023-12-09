import typer
import logging

from . import __version__
from .utils import DebugOption, VerboseOption, QuietOption, verbose_args_processor
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
