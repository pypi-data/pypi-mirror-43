from typing import get_type_hints, List, Dict
import json
import sys

def __default_help_menu(error, args, trigger):
    if error is not None:
        print(f'{error}\n')

    print('Valid Arguments:')
    for arg in args:
        line = f'\t{arg.shortname}'
        
        if arg.longname:
            line += f' ({arg.longname})'

        line += ' - '

        if arg.is_flag:
            line += 'FLAG '
        
        if arg.is_required:
            line += 'REQUIRED '
        elif not arg.is_flag:
            line += 'OPTIONAL '

        if arg.default:
            line += f'DEFAULT: {arg.default}'

        print(line)

    print(f'Specify "{trigger}" to see this again.')

def __convert_to_type(value, to_type):
    try:
        if to_type is dict or to_type is Dict or to_type is list or to_type is List:
            raise NotImplementedError
        else:
            return to_type(value)
    except ValueError:
        return None

def __handle_argument_map(arg_map: List, hints: Dict) -> List:
    if len(arg_map) != len(hints):
        raise AssertionError('Uneven number of arguments to entrypoint function parameters.')

    types = list(hints.values())

    arguments = []
    for i, arg in enumerate(arg_map):
        value = arg.gather_value(sys.argv)
        arguments.append(__convert_to_type(value, types[i]))

    return arguments

def __handle_main(func, arg_map: List, help_func=__default_help_menu, help_trigger='-h'):
    # We don't care about arguments, as if they dont want to use them they shouldn't
    # have to specify them.
    hints = get_type_hints(func)
    main_return = hints.pop('return', str)
    if main_return is not int and main_return is not type(None):
        raise TypeError('Entrypoint functions must return an integer value or "None".')

    if help_trigger in sys.argv:
        help_func(None, arg_map, help_trigger)
        return 1
    elif type(arg_map) is list:
        try:
            result = func(*__handle_argument_map(arg_map, hints))
        except AttributeError as e:
            if callable(help_func):
                help_func(e, arg_map, help_trigger)
                return 1
            else:
                raise e
    else:
        result = func(sys.argv, len(sys.argv))

    exit(result if type(result) is int else 0)
