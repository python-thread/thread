import logging
from colorama import init, Fore, Style

init(autoreset = True)


# Stdout color config #
class ColorFormatter(logging.Formatter):
  COLORS = {
    'DEBUG'   : Fore.BLUE,
    'INFO'    : Fore.GREEN,
    'WARNING' : Fore.YELLOW,
    'ERROR'   : Fore.RED,
    'CRITICAL': Fore.RED + Style.BRIGHT
  }

  def format(self, record):
    color = self.COLORS.get(record.levelname, '')
    if color:
      record.levelname = color + Style.BRIGHT + f'{record.levelname:<9}|'
      record.msg = color + Fore.WHITE + Style.NORMAL + record.msg
    return logging.Formatter.format(self, record)


class ColorLogger(logging.Logger):
  def __init__(self, name):
    logging.Logger.__init__(self, name, logging.DEBUG)
    color_formatter = ColorFormatter('%(levelname)s %(message)s' + Style.RESET_ALL)
    console = logging.StreamHandler()
    console.setFormatter(color_formatter)
    self.addHandler(console)
