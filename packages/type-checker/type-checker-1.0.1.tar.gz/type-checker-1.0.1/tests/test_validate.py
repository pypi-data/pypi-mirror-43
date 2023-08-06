from typing import Optional, Union, List, Any, Type, Dict, Callable

from type_checker.converters import StringToUUIDConverter, \
    StringToIntConverter, StringToDateConverter, StringToFloatConverter
from type_checker.validate import validate


class TestValidator:

    def test_basic(self):
        assert validate("hey", str)
        assert not validate("hey", int)

    def test_union(self):
        type_def = Union[int, str]
        assert validate("hey", type_def)
        assert validate(1, type_def)
        assert not validate(0.1, type_def)

    def test_any(self):
        type_def = Any

        class Person:
            pass

        assert validate("hey", type_def)
        assert validate(1, type_def)
        assert validate(Person, type_def)
        assert validate(Person(), type_def)

    def test_type(self):
        type_def = Type

        class Person:
            pass

        assert validate(Person, type_def)
        assert not validate(1, type_def)
        assert not validate(Person(), type_def)

    def test_instance(self):
        class Person:
            pass

        type_def = Person

        assert not validate(Person, type_def)
        assert not validate(1, type_def)
        assert validate(Person(), type_def)

    def test_optional(self):
        type_def = Optional[int]
        assert not validate("hey", type_def)
        assert validate(1, type_def)
        assert validate(None, type_def)

    def test_optional_union(self):
        type_def = Optional[Union[int, float]]
        assert not validate("hey", type_def)
        assert validate(1, type_def)
        assert validate(1.1, type_def)
        assert validate(None, type_def)

    def test_list(self):
        type_def = [int]

        model = [1, 2, 3, 4]
        assert validate(model, type_def)

        model = [1, "two", 3, 4]
        assert not validate(model, type_def)

    def test_list_nested(self):
        type_def = [[int]]

        model = [[1, 2, 3, 4]]
        assert validate(model, type_def)

        model = [[1, "two", 3, 4]]
        assert not validate(model, type_def)

    def test_list_nested_union(self):
        type_def = [Union[str, List[int]]]

        model = ["one", [2, 3, 4]]
        assert validate(model, type_def)

        model = [1, [2, 3, 4]]
        assert not validate(model, type_def)

    def test_set(self):
        type_def = {int}

        model = {1, 2, 3}
        assert validate(model, type_def)

        model = {1, "two", 3, 4}
        assert not validate(model, type_def)

    def test_tuple(self):
        type_def = (int,)

        model = (1, 2, 3)
        assert validate(model, type_def)

        model = (1, "two", 3, 4)
        assert not validate(model, type_def)

    def test_tuple_union(self):
        type_def = (int, str)

        model = (1, "two", 3, 4)
        assert validate(model, type_def)

    def test_dict(self):
        type_def = {
            "value": int
        }

        model = {
            "value": 10
        }
        assert validate(model, type_def)

    def test_dict_optional(self):
        type_def = {
            "value": int,
            Optional["opt"]: str
        }

        model = {
            "value": 10
        }
        assert validate(model, type_def)

        model_2 = {
            "value": 10,
            "opt": "valid"
        }
        assert validate(model_2, type_def)

        model_3 = {
            "value": 10,
            "opt": 15
        }

        assert not validate(model_3, type_def)

    def test_dict_nested(self):
        type_def = {
            "value": {
                str: int
            }
        }

        model = {
            "value": {
                "test": 1,
                "test_2": 10
            }
        }
        assert validate(model, type_def)

    def test_typing_list(self):
        type_def = List[int]

        model = [1, 2, 3, 4]
        assert validate(model, type_def)

        model = [1, "two", 3, 4]
        assert not validate(model, type_def)

    def test_typing_dict(self):
        type_def = Dict[str, str]

        model = {
            "name": "rob"
        }
        assert validate(model, type_def)

        model = {
            "name": 1
        }
        assert not validate(model, type_def)

    def test_generic_typing(self):
        type_def = List[Dict[str, str]]

        model = [{
            "name": "rob"
        }]
        assert validate(model, type_def)

        model = [{
            "name": 1
        }]
        assert not validate(model, type_def)

    def test_basic_callable_typing(self):
        type_def = Callable

        def model():
            return "hey"

        assert validate(model, type_def)

        model = "hey"
        assert not validate(model, type_def)

    def test_callable_typing(self):
        type_def = Callable[[str, int], str]

        def model(hey: str, hi: int) -> str:
            return hey + str(hi)

        assert validate(model, type_def)

        def model(hey: int, hi: int) -> str:
            return str(hey) + str(hi)

        assert not validate(model, type_def)

        def model(hey: str, hi: int) -> int:
            return int(hey) + hi

        assert not validate(model, type_def)

        def model(hey: str) -> str:
            return hey

        assert not validate(model, type_def)

    def test_dict_and_generic_typing(self):
        type_def = {"test": List[Dict[str, str]]}

        model = {
            "test": [{
                "name": "rob"
            }]
        }
        assert validate(model, type_def)

        model = {
            "test": [{
                "name": 1
            }]
        }
        assert not validate(model, type_def)

    def test_validate_with_converter(self):

        type_def = {
            "identifier": StringToUUIDConverter(),
            "age": StringToIntConverter(),
            "date_of_birth": StringToDateConverter(),
            "favourite_numbers": [
                StringToDateConverter(),
                StringToFloatConverter()
            ]
        }

        data = {
            "identifier": "0640ac53-e81f-49cc-9f36-f68db7b355fc",
            "age": "26",
            "date_of_birth": "1/1/1981",
            "favourite_numbers": ["5", "7", "15.2"]
        }

        assert validate(data, type_def)
