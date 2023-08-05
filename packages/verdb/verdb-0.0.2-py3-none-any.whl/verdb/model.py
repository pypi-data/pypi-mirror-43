from collections import OrderedDict
from itertools import chain, repeat, islice
from pathlib import Path
from typing import get_type_hints

from ruamel.yaml import YAML

from .modelmeta import ModelMeta
from .modelset import ModelSet
from .section import Section


# TODO: Sync to external nodes


class Model(Section):
    meta = None

    def __init_subclass__(cls, prefix=None, **kwargs):
        cls.meta = ModelMeta(cls, prefix=prefix)
        super().__init_subclass__(**kwargs)

    def __init__(self, _=None, *, key=None, **kwargs):
        self.key = key
        self.__loaded_key = None
        self.version = None

        super().__init__(_=None, **kwargs)

    def __repr__(self):
        if not self.__loaded_key and self.version:
            return f'{type(self).__name__}.reference(key={self.key!r}, version={self.version!r})'
        else:
            return super().__repr__().replace('(', f'(key={self.key!r}, ', 1)

    def __getattribute__(self, name):
        loaded_key = object.__getattribute__(self, '_Model__loaded_key')
        version = object.__getattribute__(self, 'version')

        if not loaded_key and version and name in get_type_hints(type(self)):
            object.__getattribute__(self, '_Model__load')()
            assert object.__getattribute__(self, '_Model__loaded_key')

        return object.__getattribute__(self, name)

    def __eq__(self, other):
        assert type(self) == type(other)
        if self.__is_reference or other.__is_reference:
            return (self.__is_reference or not self.dirty) and \
                   (other.__is_reference or not other.dirty) and \
                   self.version == other.version
        else:
            return super().__eq__(other)

    @property
    def __file(self):
        if self.key:
            return self.meta.path(key=self.key)
        else:
            raise ValueError('Missing key for model')

    @property
    def __loaded_file(self):
        if self.__loaded_key:
            return self.meta.path(key=self.__loaded_key)
        else:
            return None

    @property
    def __is_reference(self):
        return self.__loaded_key and self.version

    @classmethod
    def all(cls, version='HEAD'):
        files = cls.meta.git('ls-tree', '--name-only', f'{version}:{cls.meta.path()}')
        files = map(lambda file: Path(cls.meta.directory, file), files)
        return ModelSet(cls.meta, files, version)

    @classmethod
    def reference(cls, key, version='HEAD'):
        model = cls(_=True, key=key)
        model.version = cls.meta.git('rev-list', '--max-count=1', version, '--', model.__file)
        return model

    @classmethod
    def load(cls, key, version='HEAD'):
        return cls.reference(key=key, version=version).__load()

    def __load(self):
        data = YAML(typ='safe').load(self.meta.git('show', f'{self.version}:{self.__file}'))
        self.deserialize(data, version=self.version)
        self.__loaded_key = self.key
        self.dirty = False
        return self

    def versions(self):
        if self.__loaded_key:
            commits = self.meta.git('log', '--format=oneline', '--follow', self.version, '--', self.__loaded_file)
            return OrderedDict(islice(chain(line.split(maxsplit=1), repeat('')), 2) for line in commits.splitlines())
        else:
            return OrderedDict()

    def save(self, message=''):
        with self.meta.git_context(message) as work_tree:
            file = Path(work_tree, self.__file)
            file.parent.mkdir(parents=True, exist_ok=True)

            with file.open('w', encoding='utf-8') as handle:
                YAML(typ='safe').dump(self.serialize() or {}, handle)

            if self.__loaded_key and self.key != self.__loaded_key:
                self.meta.git('rm', self.__loaded_file)

            self.__loaded_key = self.key
            self.meta.git('add', file)

        self.version = self.meta.git('rev-parse', 'HEAD')
        self.dirty = False

    def delete(self, message=''):
        with self.meta.git_context(message) as work_tree:
            file = Path(work_tree, self.__file)
            self.meta.git('rm', file)

        self.version = None
