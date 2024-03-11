class Settings:
  """
  # Settings
  `Non Instantiable`
  """

  VERBOSITY: bool = True
  GRACEFUL_EXIT_ENABLED: bool = True

  def __init__(self):
    raise NotImplementedError('This class is not instantiable')

  @staticmethod
  def set_graceful_exit(enabled: bool = True):
    Settings.GRACEFUL_EXIT_ENABLED = enabled

  @staticmethod
  def set_verbosity(verbosity: bool = True):
    Settings.VERBOSITY = verbosity
