class Container:
    def __str__(self):
        return type(self).__name__

    def __getitem__(self, item):
        return self.get(item)

    def __setitem__(self, key, value):
        self.set(key, value)

    def __getattr__(self, attr):
        if not attr in type(self._data).__dict__.keys():
            raise AttributeError
        return getattr(self._data, attr)

    def __init__(self):
        raise NotImplementedError

    def get(self, item=None, default=None):
        if not item:
            return self._data
        if not item in self._data:
            return default
        return self._data[item]


class Cache(type):
    instances = {}

    def __call__(cls, *args, **kwargs):
        if not args[0] in cls.instances:
            cls.instances[args[0]] = super(Cache, cls).__call__(*args, **kwargs)
        return cls.instances[args[0]]


class CachedObj(Container, metaclass=Cache):
    def __init__(self, obj_id, data=None, **kwargs):
        self._data = data if data else self.default_handler(obj_id, **kwargs)
        self.id = obj_id

    def default_handler(self, **kwargs):
        return None


class Loader(Container):
    def __init__(self, **kwargs):
        self._data = self.default_handler(**kwargs)

    def default_handler(self, **kwargs):
        raise NotImplementedError
