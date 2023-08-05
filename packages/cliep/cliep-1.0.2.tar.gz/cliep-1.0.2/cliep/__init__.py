from .args import Argument
from .util import __handle_main, __default_help_menu

name = 'cliep'

def entrypoint(arg_map: list, help_func=__default_help_menu, help_trigger='-h'):
    # If we're getting passed a function, run, else handle wrap main handling and return that.
    if callable(arg_map):
        __handle_main(arg_map, None, help_func, help_trigger)
    else:
        def actual(func):
            __handle_main(func, arg_map, help_func, help_trigger)

        return actual