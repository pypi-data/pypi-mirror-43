from collections import OrderedDict
from itertools import chain, repeat, islice
from pathlib import Path
from subprocess import CalledProcessError

from ruamel.yaml import YAML

from .modelmeta import ModelMeta
from .modelset import ModelSet
from .section import Section


# TODO: Sync to external nodes
# TODO: Check if sync race conditions can be handled with vector clocks


class Model(Section):
    meta = None

    def __init_subclass__(cls, prefix=None, **kwargs):
        cls.meta = ModelMeta(cls, prefix=prefix)
        super().__init_subclass__(**kwargs)

    def __init__(self, key=None, **kwargs):
        super().__init__(**kwargs)

        self.key = key
        self.__loaded_key = None
        self.__version = None

    def __repr__(self):
        return super().__repr__().replace('(', f'(key={self.key!r}, ', 1)

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

    @classmethod
    def all(cls, version='HEAD'):
        files = cls.meta.git('ls-tree', '--name-only', f'{version}:{cls.meta.directory}')
        files = map(lambda file: Path(cls.meta.directory, file), files)
        return ModelSet(cls.meta, files, version)

    @classmethod
    def load(cls, key, version='HEAD'):
        data = YAML(typ='safe').load(cls.meta.git('show', f'{version}:{cls.meta.path(key=key)}'))

        model = cls.deserialize(data)
        model.key = model.__loaded_key = key
        model.__version = cls.meta.git('rev-parse', version)

        return model

    @property
    def version(self):
        return self.__version

    def versions(self):
        if self.__loaded_key:
            commits = self.meta.git('log', '--format=oneline', '--follow', self.version, '--', self.__loaded_file)
            return OrderedDict(islice(chain(line.split(maxsplit=1), repeat('')), 2) for line in commits.splitlines())
        else:
            return OrderedDict()

    def save(self, message=''):
        with self.meta.git_context(message) as (index, work_tree):
            file = Path(work_tree, self.__file)
            file.parent.mkdir(parents=True, exist_ok=True)

            with file.open('w', encoding='utf-8') as handle:
                YAML(typ='safe').dump(self.serialize() or {}, handle)

            if self.__loaded_key and self.key != self.__loaded_key:
                loaded_file = Path(work_tree, self.__loaded_file)
                self.meta.git('rm', str(loaded_file.resolve()), work_tree=work_tree, index_file=index)

            self.__loaded_key = self.key
            self.meta.git('add', str(file.resolve()), work_tree=work_tree, index_file=index)

        self.__version = self.meta.git('rev-parse', 'HEAD')

    def delete(self, message=''):
        with self.meta.git_context(message) as (index, work_tree):
            file = Path(work_tree, self.__file)
            self.meta.git('rm', str(file.resolve()), work_tree=work_tree, index_file=index)

        self.__version = None
