__version__ = '0.3.1'

from os import getcwd
from copy import deepcopy
from functools import reduce

from abconfig.common import Container
from abconfig.loaders import File, Env


class ABConfig(Container):
    file = getcwd() + '/config'
    loaders = (File, Env,)
    _reserved_attr = (
        'loaders',
        'file',
    )

    def __init__(self, prefix=None, **kwargs):
        if type(self).__name__ == 'ABConfig':
            raise NotImplementedError

        self.prefix = prefix
        self._data = self.get_config(**self._attrs(self, **kwargs))

    def get_config(self, **kwargs):
        result = dict()
        for name, defaults in kwargs.items():
            result.update(self._load_config(name, defaults))
        return result

    def _load_config(self, name, defaults):
        values = deepcopy(defaults)
        for loader in self.loaders:
            prefix = self.prefix if self.prefix else None
            if reduce(lambda a, b: a or b,
                    map(lambda x: isinstance(values, x), (int, str, bool, list, tuple))):
                read = loader(prefix=prefix, defaults=(name,), path=self.file).get()
                if read: values = read[name]

            elif isinstance(values, dict):
                read = loader(prefix=name, defaults=defaults.keys(), path=self.file).get()
                if read: values.update(read)

        return {name: values}

    def _attrs(self, obj, **kwargs):
        result = {}
        for attr in type(obj).__dict__.keys():
            if (attr[:2] != '__' and attr[:1] != '_' and
                    attr not in self._reserved_attr):
                result.update({str(attr): getattr(self, attr)})

        if kwargs:
            result.update(kwargs)
        return result
