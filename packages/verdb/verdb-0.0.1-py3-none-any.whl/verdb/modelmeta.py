import platform
from contextlib import contextmanager
from pathlib import Path
from subprocess import run, CalledProcessError
from tempfile import TemporaryDirectory
from weakref import ref


class ModelMeta:
    def __init__(self, model, prefix):
        self._model = ref(model)
        self.prefix = prefix

    @property
    def model(self):
        return self._model()

    def path(self, key=None):
        if key:
            return Path(f'{self.model.__name__.lower()}s', f'{key}.yml')
        else:
            return Path(f'{self.model.__name__.lower()}s')

    @property
    def directory(self):
        return Path(self.prefix, self.path())

    def git(self, *args, **kwargs):
        command = ['git'] + [str(arg) for arg in args if arg]
        env = {
            **{f'GIT_{key.upper()}': str(value) for key, value in kwargs.items() if value},
            **{'GIT_DIR': str(Path(self.prefix, '.git').resolve())}
        }
        result = run(command, env=env, capture_output=True)

        try:
            result.check_returncode()
            return result.stdout.decode('utf-8').strip()
        except CalledProcessError:
            raise ValueError(result.stderr.decode('utf-8').strip())

    @contextmanager
    def git_context(self, message):
        with TemporaryDirectory() as index, TemporaryDirectory() as work_tree:
            index = str(Path(index, 'index').resolve())
            self.git('reset', index_file=index)
            yield index, work_tree
            self.git(
                'commit',
                '--allow-empty',
                '--allow-empty-message',
                f'--message={message}',
                index_file=index,
                author_name='VerDB',
                author_email=f'verdb@{platform.node()}',
                committer_name='VerDB',
                committer_email=f'verdb@{platform.node()}')
