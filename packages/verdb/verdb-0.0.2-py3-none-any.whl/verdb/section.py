from base64 import b64encode, b64decode
from enum import Enum
from typing import get_type_hints, Union

import verdb.model


class Section:
    def __init__(self, _=None, **kwargs):
        self.__dirty = True

        if _:
            return

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
        def repr_(field):
            value = getattr(self, field)
            if isinstance(value, verdb.model.Model):
                return f'{type(value).__name__}(key={value.key!r}, version={value.version!r})'
            else:
                return repr(value)

        return f'{type(self).__name__}(' + \
            ', '.join(f'{field}={repr_(field)}' for field in get_type_hints(type(self))) + \
            ')'

    def __eq__(self, other):
        assert type(self) == type(other)
        return all(getattr(self, field) == getattr(other, field) for field in get_type_hints(type(self)))

    def __setattr__(self, name, value):
        if name in get_type_hints(type(self)):
            self.__dirty = True

        super().__setattr__(name, value)

    @property
    def dirty(self):
        return self.__dirty or \
               any(getattr(self, key).dirty
                   for key, field in get_type_hints(type(self)).items()
                   if isinstance(field, type) and
                   issubclass(field, Section) and
                   not issubclass(field, verdb.model.Model))

    @dirty.setter
    def dirty(self, value):
        self.__dirty = False
        for key, field in get_type_hints(type(self)).items():
            if isinstance(field, type) and \
               issubclass(field, Section) and \
               not issubclass(field, verdb.model.Model):
                setattr(getattr(self, key), 'dirty', value)

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
                    return [map_to_value(field_name, field.__args__[0], value)
                            for value in value] or None

                elif field.__origin__ is dict:
                    return {map_to_value(field_name, field.__args__[0], key):
                            map_to_value(field_name, field.__args__[1], value)
                            for key, value in value.items()} or None

                raise ValueError(f'Type {field} is unsupported')

            elif issubclass(field, verdb.model.Model):
                return value.key

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

        type_hints = get_type_hints(type(self))
        data = {key: map_to_value(key, model, getattr(self, key)) for key, model in type_hints.items()}
        data = {key: value for key, value in data.items() if value is not None}
        return data if data else None

    def deserialize(self, data, version=None):
        def map_to_model(field, value):
            if hasattr(field, '__origin__'):
                if field.__origin__ is Union:
                    for option in field.__args__:
                        try:
                            return map_to_model(option, value)
                        except (TypeError, ValueError):
                            pass

                elif field.__origin__ is list:
                    return [map_to_model(field.__args__[0], value)
                            for value in value]

                elif field.__origin__ is dict:
                    return {map_to_model(field.__args__[0], key):
                            map_to_model(field.__args__[1], value)
                            for key, value in value.items()}

                raise ValueError(f'Type {field} is unsupported')

            elif issubclass(field, verdb.model.Model):
                return field.reference(key=value, version=version)

            elif issubclass(field, Section):
                return field(value).deserialize(value)

            elif field is bytes:
                return b64decode(value)

            elif value is not None:
                return field(value)

            elif field is type(None):
                return None

            else:
                raise ValueError(f"Can't convert {value} to {field}")

        for key, model in get_type_hints(type(self)).items():
            setattr(self, key, map_to_model(model, data.get(key)))

        return self
