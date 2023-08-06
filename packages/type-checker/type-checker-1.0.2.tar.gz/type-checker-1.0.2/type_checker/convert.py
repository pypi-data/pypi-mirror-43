from typing import Any

from type_checker.validate import type_check


def convert(value, type_def, base=None) -> Any:
    return type_check(
        value=value,
        type_def=type_def,
        base=base,
        raise_error=True,
        convert=True
    )
