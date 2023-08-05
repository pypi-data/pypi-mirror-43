import yaml
import json

from os import path
from .common import CachedObj


class File(CachedObj):
    def exists(self, obj_id):
        filename, extension = path.splitext(obj_id)
        if not extension:
            if path.exists(filename) is False:
                return obj_id + '.' + type(self).__name__.lower()
        return obj_id


class Yaml(File):
    def default_handler(self, obj_id, **kwargs):
        with open(self.exists(obj_id), 'r') as file:
            return yaml.load(file)


class Json(File):
    def default_handler(self, obj_id, **kwargs):
        with open(self.exists(obj_id), 'r') as file:
            return json.load(file)
