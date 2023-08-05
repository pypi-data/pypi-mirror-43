class ModelSet:
    def __init__(self, meta, files, version):
        self.model = meta.model
        self.keys = [file.stem for file in files]
        self.version = version

    def __repr__(self):
        return '[' + ', '.join(f'<{self.model.__name__}: {key!r}>' for key in self.keys) + ']'

    def __getitem__(self, item):
        assert item in self.keys
        return self.model.load(item, version=self.version)

    def __iter__(self):
        return (self.model.load(key, version=self.version) for key in self.keys)
