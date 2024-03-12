from typing import Any, Literal, Union, Callable


_Verbosity_Num = Literal[0, 1, 2]
_Verbosity_Enum = Literal['quiet', 'normal', 'verbose']
VerbosityLevel = Union[_Verbosity_Num, _Verbosity_Enum]
VerbosityMapping: dict[_Verbosity_Enum, _Verbosity_Num] = {
    'quiet': 0,
    'normal': 1,
    'verbose': 2,
}


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
