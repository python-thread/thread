# Verbose Command Processor #
import typer
import logging


# Verbose Options #
DebugOption = typer.Option(
  False, '--debug',
  help = 'Set verbosity level to DEBUG',
  is_flag = True
)
VerboseOption = typer.Option(
  False, '--verbose', '-v',
  help = 'Set verbosity level to INFO',
  is_flag = True
)
QuietOption = typer.Option(
  False, '--quiet', '-q',
  help = 'Set verbosity level to ERROR',
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

def kwargs_processor(ctx: typer.Context) -> dict:
  """Processes overflow arguments into kwargs"""
  kwargs = {}
  length = len(ctx.args) // 2

  for i in range(length):
    kv_pair = ctx.args[i*2:i*2+2]
    kwargs[kv_pair[0]] = kv_pair[1]

  return kwargs


