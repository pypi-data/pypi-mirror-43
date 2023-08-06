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
        if value is None:
            return None
        elif to_type is dict or to_type is Dict or to_type is list or to_type is List:
            raise NotImplementedError
        else:
            return to_type(value)
    except (ValueError, TypeError,):
        return None

def __handle_argument_map(arg_map: List, hints: Dict, help_func, help_trig) -> List:
    if len(arg_map) != len(hints):
        raise AssertionError('Uneven number of arguments to entrypoint function parameters.')

    types = list(hints.values())

    arguments = []
    for i, arg in enumerate(arg_map):
        value = __convert_to_type(arg.gather_value(sys.argv), types[i])
        if arg.is_required and value is None:
            help_func(f'Required argument {arg.shortname} failed to be processed (expects {types[i].__name__}).', arg_map, help_trig)
            return 2
        else:
            arguments.append(value)

    return arguments

def __handle_main(func, arg_map: List, help_func=__default_help_menu, help_trigger='-h'):
    # TODO: Possibly allow for non type hinted arguments?
    hints = get_type_hints(func)
    main_return = hints.pop('return', str)
    if main_return is not int and main_return is not type(None):
        raise TypeError('Entrypoint functions must return an integer value or "None".')

    if help_trigger in sys.argv:
        help_func(None, arg_map, help_trigger)
        result = 1
    elif type(arg_map) is list:
        try:
            arguments = __handle_argument_map(arg_map, hints, help_func, help_trigger)

            if type(arguments) is int:
                result = arguments
            else:
                result = func(*arguments)
        except AttributeError as e:
            if callable(help_func):
                help_func(e, arg_map, help_trigger)
                result = 1
            else:
                raise e
    else:
        result = func(sys.argv, len(sys.argv))

    exit(result if type(result) is int else 0)
