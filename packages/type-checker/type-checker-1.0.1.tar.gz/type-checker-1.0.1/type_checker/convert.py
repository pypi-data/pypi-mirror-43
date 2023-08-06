from typing import Any

from type_checker.validate import validate


def convert(value, type_def, base=None) -> Any:
    return validate(
        value=value,
        type_def=type_def,
        base=base,
        raise_error=True,
        convert=True
    )
