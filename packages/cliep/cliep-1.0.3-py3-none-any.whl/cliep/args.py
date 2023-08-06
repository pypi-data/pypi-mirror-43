from typing import List, Dict

class Argument(object):
    __slots__ = ['_shortname', '_longname', '_is_flag', '_value', '_required', '_default']

    def __init__(self, shortname: str, longname: str=None, is_flag: bool=False, is_required: bool=False, default=None):
        self._shortname = shortname
        self._longname = longname
        self._is_flag = is_flag
        self._required = is_required
        self._default = default

    def _get_argument_index(self, argv: List) -> int:
        # Gross but it works.
        try:
            return argv.index(self._shortname)
        except ValueError:
            pass

        try:
            return argv.index(self._longname)
        except ValueError:
            return -1

    def _gather_flag_value(self, argv: List) -> int:
        self._value = self._shortname in argv
        if not self._value and self._longname:
            self._value = self._longname in argv
        
        if self._required and not self._value:
            raise AttributeError('Required flag is not present. Are you sure you\'re using this right?')
        
        return self._value

    def _gather_string_value(self, argv: List) -> str:
        proper_index = self._get_argument_index(argv)
        if proper_index < 0:
            if self._required:
                raise AttributeError(f'Required argument {self._shortname} is not present.')
            self._value = self._default
            return self._value
        else:
            proper_index += 1
            
        if proper_index >= len(argv) or argv[proper_index][0] == '-':
            if self._required:
                raise ValueError(f'Required argument {self._shortname} is missing a value.')
            else:
                self._value = self._default
        else:
            self._value = argv[proper_index]

        return self._value

    def gather_value(self, argv: List) -> [bool, str]:
        if self._is_flag:
            return self._gather_flag_value(argv)
        else:
            return self._gather_string_value(argv)

    @property
    def shortname(self) -> str:
        return self._shortname

    @property
    def longname(self) -> str:
        return self._longname

    @property
    def is_flag(self) -> bool:
        return self._is_flag

    @property
    def is_required(self) -> bool:
        return self._required

    @property
    def default(self): 
        return self._default