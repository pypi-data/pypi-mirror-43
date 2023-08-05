from hvac import Client
from .common import CachedObj


class Vault(CachedObj):
    def _isenable(self, enabled=False) -> bool:
        if (enabled is False or enabled == 'False'
                or enabled == 'false'):
            return False
        return True

    def default_handler(self, prefix, **kwargs):
        kv_version = int(kwargs.get('kv_version', 1))
        environment = kwargs.get('environment', None)
        env = 'default' if not environment else environment
        path = kwargs['path']

        if env != 'default' and path.endswith(env) is False: path += '/' + env
        if self._isenable(kwargs.get('enabled', False)) is False: return dict()

        client = Client(url=kwargs['addr'], token=kwargs['token'])
        if kv_version == 1:
            return client.read(path)['data']
        elif kv_version == 2:
            return client.secrets.kv.v2.read_secret_version(path)['data']['data']

