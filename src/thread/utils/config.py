from typing import Any, Callable, Literal, Union, cast

_Verbosity_Num = Literal[0, 1, 2]
_Verbosity_Enum = Literal['quiet', 'normal', 'verbose']
VerbosityLevel = Union[_Verbosity_Num, _Verbosity_Enum]
VerbosityMapping: dict[_Verbosity_Enum, _Verbosity_Num] = {
    'quiet': 0,
    'normal': 1,
    'verbose': 2,
}


class Verbosity:
    """
    # Verbosity

    Can be instantiated with and compared against a number or an enum.
    """

    level_number: _Verbosity_Num
    level_string: _Verbosity_Enum

    def __init__(self, level: VerbosityLevel) -> None:
        """
        Initializes the verbosity object.

        Parameters
        ----------
        :param level: The level of verbosity. Can be a number or an enum.

        Raises
        ------
        ValueError: If the level is not a valid number or enum.
        ValueError: If the level is not of a valid type.
        """
        if isinstance(level, str):
            if level not in VerbosityMapping.keys():
                raise ValueError('Invalid verbosity level')
            self.level_string = level
            self.level_number = VerbosityMapping[level]
        elif isinstance(level, int):
            if level not in VerbosityMapping.values():
                raise ValueError('Invalid verbosity level')
            self.level_number = level
            self.level_string = list(VerbosityMapping.keys())[level]
        else:
            raise ValueError(f'{type(level)} is not a valid verbosity level')

    def __str__(self) -> str:
        return self.level_string

    def __eq__(self, other: Any) -> bool:
        try:
            return self._compare(other, lambda a, b: a == b)
        except ValueError:
            return False

    def __lt__(self, other: Any) -> bool:
        return self._compare(other, lambda a, b: a < b)

    def __le__(self, other: Any) -> bool:
        return self._compare(other, lambda a, b: a <= b)

    def __gt__(self, other: Any) -> bool:
        return self._compare(other, lambda a, b: a > b)

    def __ge__(self, other: Any) -> bool:
        return self._compare(other, lambda a, b: a >= b)

    def __ne__(self, other: Any) -> bool:
        return not self.__eq__(other)

    def _compare(
        self, other: Any, operator: Callable[[VerbosityLevel, Any], bool]
    ) -> bool:
        if isinstance(other, Verbosity):
            return operator(self.level_number, other.level_number)
        if isinstance(other, int):
            return operator(self.level_number, other)
        if isinstance(other, str):
            if Verbosity.is_valid_level(other):
                other = cast(_Verbosity_Enum, other)
                return operator(self.level_number, VerbosityMapping[other])
            return operator(self.level_string, other)
        raise ValueError('Cannot compare Verbosity with other types')

    @staticmethod
    def is_valid_level(level: Any) -> bool:
        """
        Determines whether the given level is a valid verbosity level.

        Parameters
        ----------
        :param level: The level to check.

        Returns
        -------
        :returns: True if the level is a valid verbosity level, False otherwise.
        """
        if isinstance(level, int):
            return level in VerbosityMapping.values()
        if isinstance(level, str):
            return level in VerbosityMapping.keys()
        return False


class Settings:
    """
    # Settings
    `Non Instantiable`
    """

    # Verbosity
    VerbosityLevel = VerbosityLevel
    VERBOSITY: Verbosity = Verbosity(1)

    # Graceful Exit
    GRACEFUL_EXIT_ENABLED: bool = True

    def __init__(self):
        raise NotImplementedError('This class is not instantiable')

    @staticmethod
    def set_graceful_exit(enabled: bool = True) -> None:
        """
        Enables/Disables graceful exiting.

        Parameters
        ----------
        :param enabled: True to enable graceful exit, False otherwise.

        Returns
        -------
        :returns: None
        """
        Settings.GRACEFUL_EXIT_ENABLED = enabled

    @staticmethod
    def set_verbosity(verbosity: VerbosityLevel = 'normal') -> None:
        """
        Sets the verbosity level.

        Parameters
        ----------
        :param verbosity: The level of verbosity. Can be a number or an enum.

        Returns
        -------
        :returns: None

        Raises
        ------
        ValueError: If the level is not a valid number or enum.
        ValueError: If the level is not of a valid type.
        """
        Settings.VERBOSITY = Verbosity(verbosity)
