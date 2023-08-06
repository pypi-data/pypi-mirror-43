import uuid

from datetime import datetime, date
from uuid import UUID


class BaseConverter:

    def __init__(self, input_type_def, output_type_def):
        self.input_type_def = input_type_def
        self.output_type_def = output_type_def

    def convert(self, value):
        raise NotImplementedError


class StringToUUIDConverter(BaseConverter):

    def __init__(self):
        super().__init__(input_type_def=str, output_type_def=UUID)

    def convert(self, value: str) -> UUID:
        return uuid.UUID(value)


class StringToIntConverter(BaseConverter):

    def __init__(self, check_digit=True):
        self.check_digit = check_digit
        super().__init__(input_type_def=str, output_type_def=int)

    def convert(self, value: str) -> int:
        if self.check_digit:
            if not value.isdigit():
                raise ValueError(f"StringToIntConverter expecting a digit, "
                                 f"got {value}")
        return int(value)


class StringToFloatConverter(BaseConverter):

    def __init__(self):
        super().__init__(input_type_def=str, output_type_def=float)

    def convert(self, value: str) -> float:
        return float(value)


class StringToDateConverter(BaseConverter):

    def __init__(self, date_format='%m/%d/%Y'):
        self.date_format = date_format
        super().__init__(input_type_def=str, output_type_def=date)

    def convert(self, value: str) -> date:
        return datetime.strptime(value, self.date_format).date()


class Convert(BaseConverter):

    converters = {
        (converter.input_type_def, converter.output_type_def): converter
        for converter in [
            StringToUUIDConverter(),
            StringToIntConverter(),
            StringToFloatConverter(),
            StringToDateConverter()
        ]
    }

    def __init__(self, input_type_def, output_type_def):
        self.converter = self.converters[(input_type_def, output_type_def)]
        super().__init__(input_type_def, output_type_def)

    def convert(self, value):
        return self.converter.convert(value=value)
