import typing
from _ast import Set
from inspect import isclass
from typing import List, Tuple, Any, Type, Dict, Callable

import typing_inspect

from type_checker.converters import BaseConverter


def validate(
    value,
    type_def,
    raise_error=False,
    base=None,
    convert=False,
    convert_to_validate=True
) -> bool:

    if base is None:
        base = value

    def response(valid):
        if valid and convert:
            return value
        return valid

    if type_def == Any:
        return response(True)

    type_def = getattr(type_def, '__forward_arg__', type_def)

    if isinstance(type_def, BaseConverter):
        if convert_to_validate:
            value = type_def.convert(value=value)

        type_def = type_def.output_type_def

    def raise_or_return_false(error):
        if raise_error or convert:
            raise error(f"Invalid type {base}, "
                        f"error in {value}.\nExpecting {type(type_def)}, "
                        f"found {type(value)}")

        return False

    if type_def == Type:
        if not isclass(value):
            return raise_or_return_false(TypeError)

    if isclass(type_def):
        origin = None

        # noinspection PyBroadException
        try:
            origin = typing_inspect.get_origin(type_def)
        except Exception:
            pass

        if origin and issubclass(origin, (List, Set, Tuple)):
            args = type_def.__args__
            type_def = [args[0]]

        elif origin and issubclass(origin, Dict):
            args = type_def.__args__
            type_def = {args[0]: args[1]}

        elif origin and issubclass(origin, Callable):
            args = type_def.__args__

            if not callable(value):
                return raise_or_return_false(TypeError)

            if not args:
                return response(True)

            type_hints = typing.get_type_hints(value)
            args = list(args)
            values = list(type_hints.values())
            if args != values:
                return raise_or_return_false(TypeError)

            return response(True)

        else:
            if not isinstance(value, type_def):
                return raise_or_return_false(TypeError)
            return response(True)

    if typing_inspect.is_union_type(type_def):
        _type_maps = typing_inspect.get_args(type_def, evaluate=True)
        valid = False
        for _type_map in _type_maps:
            # noinspection PyBroadException
            try:
                if validate(value=value,
                            type_def=_type_map,
                            raise_error=raise_error,
                            base=base):
                    valid = True
                    break
            except Exception:
                pass
        if not valid:
            return raise_or_return_false(TypeError)

        return response(True)

    if isinstance(type_def, (list, set, tuple)):
        if not isinstance(value, (list, set, tuple)):
            return raise_or_return_false(TypeError)

        converted_values = []

        for _value in value:
            valid = False
            for _type_map in type_def:
                # noinspection PyBroadException
                try:
                    _response = validate(
                        value=_value,
                        type_def=_type_map,
                        raise_error=raise_error,
                        base=base,
                        convert=convert,
                        convert_to_validate=convert_to_validate
                    )
                    if convert or _response:
                        valid = True

                        if convert:
                            converted_values.append(_response)

                        break
                except Exception:
                    pass
            if not valid:
                return raise_or_return_false(TypeError)

        if convert:
            value = converted_values

        return response(True)

    if isinstance(type_def, dict):
        if not isinstance(value, dict):
            return raise_or_return_false(TypeError)

        converted_values = {}

        for key_type_map, value_type_map in type_def.items():
            valid = False
            corresponding_value = None
            optional = False
            converted_key = None
            converted_value = None

            if typing_inspect.is_union_type(key_type_map):
                optional = type(None) in typing_inspect.get_args(key_type_map,
                                                                 evaluate=True)
            for key_value, _value in value.items():
                # noinspection PyBroadException
                try:
                    _response = validate(
                        value=key_value,
                        type_def=key_type_map,
                        raise_error=raise_error,
                        base=base,
                        convert=convert,
                        convert_to_validate=convert_to_validate
                    )
                    if convert or _response:
                        valid = True
                        corresponding_value = _value

                        if convert:
                            converted_key = _response

                        break
                except Exception:
                    pass

            if not valid:
                if not optional:
                    return raise_or_return_false(KeyError)

            else:
                _response = validate(value=corresponding_value,
                                     type_def=value_type_map,
                                     raise_error=raise_error,
                                     base=base,
                                     convert=convert,
                                     convert_to_validate=convert_to_validate)
                if not convert and not _response:
                    return response(False)

                converted_value = _response

            if convert:
                converted_values[converted_key] = converted_value

        if convert:
            value = converted_values

        return response(True)

    if value == type_def:
        return response(True)

    return raise_or_return_false(TypeError)
