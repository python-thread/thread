class Settings:
  """
  # Settings
  `Non Instantiable`
  """

  GRACEFUL_SHUTDOWN_ENABLED: bool = True


  def __init__(self):
    raise NotImplementedError('This class is not instantiable')
  

  @staticmethod
  def set_graceful_shutdown(enabled: bool = True):
    Settings.GRACEFUL_SHUTDOWN_ENABLED = enabled
