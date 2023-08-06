import datetime
import uuid

from type_checker.converters import \
    StringToUUIDConverter, \
    StringToDateConverter, \
    StringToIntConverter, \
    StringToFloatConverter, \
    Convert

from type_checker.convert import convert


class TestConverter:

    def test_basic_convert(self):
        example_uuid = uuid.uuid4()
        example_str_uuid = str(example_uuid)
        type_def = StringToUUIDConverter()

        result = convert(example_str_uuid, type_def)

        assert result == example_uuid

    def test_lookup_convert(self):
        example_uuid = uuid.uuid4()
        example_str_uuid = str(example_uuid)

        type_def = Convert(str, uuid.UUID)

        result = convert(example_str_uuid, type_def)

        assert result == example_uuid

    def test_type_dict_convert(self):
        example_uuid = uuid.uuid4()
        example_str_uuid = str(example_uuid)

        type_def = {
            "identifier": StringToUUIDConverter()
        }

        result = convert({
            "identifier": example_str_uuid
        }, type_def)

        assert result == {
            "identifier": example_uuid
        }

    def test_type_list_convert(self):
        example_uuid = uuid.uuid4()
        example_str_uuid = str(example_uuid)

        type_def = [StringToUUIDConverter()]

        result = convert([example_str_uuid], type_def)

        assert result == [example_uuid]

    def test_multi_convert(self):
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

        result = convert(data, type_def)

        assert result == {
            "identifier": uuid.UUID("0640ac53-e81f-49cc-9f36-f68db7b355fc"),
            "age": 26,
            "date_of_birth": datetime.date(1981, 1, 1),
            "favourite_numbers": [5, 7, 15.2]
        }

    def test_multi_lookup_convert(self):
        type_def = {
            "identifier": Convert(str, uuid.UUID),
            "age": Convert(str, int),
            "date_of_birth": Convert(str, datetime.date),
            "favourite_numbers": [
                Convert(str, int),
                Convert(str, float),
                {
                    "numerator": Convert(str, int),
                    "denominator": Convert(str, int)
                }
            ]
        }

        data = {
            "identifier": "0640ac53-e81f-49cc-9f36-f68db7b355fc",
            "age": "26",
            "date_of_birth": "1/1/1981",
            "favourite_numbers": [
                "5",
                "7",
                "15.2",
                {
                    "numerator": "10",
                    "denominator": "5"
                }
            ]
        }

        result = convert(data, type_def)

        assert result == {
            "identifier": uuid.UUID("0640ac53-e81f-49cc-9f36-f68db7b355fc"),
            "age": 26,
            "date_of_birth": datetime.date(1981, 1, 1),
            "favourite_numbers": [
                5,
                7,
                15.2,
                {
                    "numerator": 10,
                    "denominator": 5
                }
            ]
        }
