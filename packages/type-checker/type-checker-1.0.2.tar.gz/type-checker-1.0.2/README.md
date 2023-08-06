# Type Checker
Type check Python types with support for nested lists and dictionaries.

[![coverage report](https://gitlab.com/robjampar/type-checker/badges/master/coverage.svg)](https://gitlab.com/robjampar/type-checker/commits/master)

[![pipeline status](https://gitlab.com/robjampar/type-checker/badges/master/pipeline.svg)](https://gitlab.com/robjampar/type-checker/commits/master)

## Installation
Type Checker is a Python package, and is compatible with `Python 3` only (for now). It can be installed through `pip`.

##### Pip
```
pip install type-checker
```

## Run the Unit Tests
To run the tests.
```
pip install pipenv
pipenv install --dev
pipenv run python -m pytest tests --cov=type_checker
```

## Docs

The documentation is public, and is generated using Sphinx.

[Type Checker Documentation](https://robjampar.gitlab.io/type-checker)

##### Build documentation
To build a local static HTML version of the documentation.
```
pip install pipenv
pipenv install sphinx
pipenv run sphinx-build docs ./public -b html
```

## Type Checking Example
``` python
from typing import Union
from type_checker import type_check

# the type defintion to check a value against
type_def = {
    "hello": {
        "world": int
    },
    "a_key": str,
    "a_list": [
        float
    ],
    int: bool,
    float: Union[bool, int]
}

# a valid test value
test_value = {
    "hello": {
        "world": 1
    },
    "a_key": "this_is_a_string",
    "a_list": [
        3.2,
        4.7
        5.9
    ],
    5: True,
    5.2: False,
    5.7: 10

}

# use validate from the type_checker package to validate the value
is_valid = type_check(test_value, type_def)

print(f"is valid: {is_valid}")
```

``` text
$ python example.py
>>> is valid: True
```
