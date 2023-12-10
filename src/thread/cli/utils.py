# Verbose Command Processor #
import typer
import logging


# Verbose Options #
DebugOption = typer.Option(
  False, '--debug',
  help = 'Set verbosity level to [blue]DEBUG[/blue]',
  is_flag = True
)
VerboseOption = typer.Option(
  False, '--verbose', '-v',
  help = 'Set verbosity level to [green]INFO[/green]',
  is_flag = True
)
QuietOption = typer.Option(
  False, '--quiet', '-q',
  help = 'Set verbosity level to [red]ERROR[/red]',
  is_flag = True
)


# Helper functions #


# Processors #
def verbose_args_processor(debug: bool, verbose: bool, quiet: bool):
  """Handles setting and raising exceptions for verbose"""
  if verbose and quiet:
    raise typer.BadParameter('--quiet cannot be used with --verbose')
  
  if verbose and debug:
    raise typer.BadParameter('--debug cannot be used with --verbose')
  
  logging.getLogger('base').setLevel((
    (debug and logging.DEBUG) or
    (verbose and logging.INFO) or
    logging.ERROR
  ))

def kwargs_processor(arguments: list[str]) -> dict[str, str]:
  """Processes arguments into kwargs"""
  return {
    kwarg[0]: kwarg[1]
    for i in arguments
    if (kwarg := i.split('='))
  }
