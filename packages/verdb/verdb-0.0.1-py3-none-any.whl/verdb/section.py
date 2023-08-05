from base64 import b64encode, b64decode
from enum import Enum
from typing import get_type_hints, Union


class Section:
    def __init__(self, _=None, **kwargs):
        for field in get_type_hints(type(self)):
            if field in kwargs:
                setattr(self, field, kwargs[field])
            elif hasattr(type(self), field):
                if callable(getattr(self.__class__, field)):
                    setattr(self, field, getattr(type(self), field)())
                else:
                    setattr(self, field, getattr(type(self), field))
            else:
                setattr(self, field, None)

    def __repr__(self):
        return f'{type(self).__name__}(' + \
            ', '.join(f'{field}={getattr(self, field)!r}' for field in get_type_hints(type(self))) + \
            ')'

    def __eq__(self, other):
        assert type(self) == type(other)
        return all(getattr(self, field) == getattr(other, field) for field in get_type_hints(type(self)))

    def serialize(self):
        def map_to_value(field_name, field, value):
            if hasattr(field, '__origin__'):
                if field.__origin__ is Union:
                    for option in field.__args__:
                        try:
                            return map_to_value(field_name, option, value)
                        except ValueError:
                            pass
                elif field.__origin__ is list:
                    values = [map_to_value(field_name, field.__args__[0], value) for value in value]
                    return values or None
                elif field.__origin__ is dict:
                    values = {map_to_value(field_name, field.__args__[0], key):
                              map_to_value(field_name, field.__args__[1], value)
                              for key, value in value.items()}
                    return values or None

                raise ValueError(f'Type {field} is unsupported')

            elif issubclass(field, Section):
                return value.serialize()

            elif field is bytes:
                return b64encode(value).decode('utf-8')

            elif issubclass(field, Enum):
                return value.value

            elif isinstance(value, field):
                return value

            elif value is None:
                raise ValueError(f'Missing value for field {field_name}')

            else:
                raise ValueError(f'{value} is not of type {field} for field {field_name}')

        type_hints = get_type_hints(self.__class__)
        data = {key: map_to_value(key, model, getattr(self, key)) for key, model in type_hints.items()}
        data = {key: value for key, value in data.items() if value is not None}
        return data if data else None

    @classmethod
    def deserialize(cls, data):
        def map_to_model(field, value):
            if hasattr(field, '__origin__'):
                if field.__origin__ is Union:
                    for option in field.__args__:
                        try:
                            return map_to_model(option, value)
                        except ValueError:
                            pass
                elif field.__origin__ is list:
                    return [map_to_model(field.__args__[0], value) for value in value]
                elif field.__origin__ is dict:
                    return {map_to_model(field.__args__[0], key): map_to_model(field.__args__[1], value)
                            for key, value in value.items()}

                raise ValueError(f'Type {field} is unsupported')

            elif issubclass(field, Section):
                type_hints = get_type_hints(field)
                fields = {key: map_to_model(model, value.get(key)) for key, model in type_hints.items()}
                return field(value, **fields)

            elif field is type(None):
                if value is not None:
                    raise ValueError()
                return None

            elif field is bytes:
                return b64decode(value)

            elif value is not None:
                return field(value)

            else:
                raise ValueError(f"Can't convert {value} to {field}")

        return map_to_model(cls, data)
