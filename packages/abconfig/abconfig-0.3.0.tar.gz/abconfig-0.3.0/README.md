### Class for creating configuration models

#### Install

```bash
pip install abconfig
```

#### File + Env

```python
>>> from abconfig import ABConfig
>>> 
>>> class DBConfig(ABConfig):
...     file = '/path/to/your/config_file.yaml'
...     postgres = dict(
...         host='127.0.0.1',
...         port='5432',
...         user='your_user',
...         password='your_pass'
...     )
... 
>>> dbconfig = DBConfig()
>>> print(dbconfig.get())
{'postgres': {'host': '127.0.0.1', 'port': '5432', 'user': 'name', 'password': 'pass'}}
>>> print(dbconfig['postgres']['host'])
'127.0.0.1'
```

#### Vault 

```python
>>> class Vault(ABConfig):
...     vault = dict(
...             kv_version=1,
...             enabled=False,
...             addr='127.0.0.1',
...             path='default/project',
...             token=False,
...     )
... 
>>> config = Vault()
>>> print(config.get())
{'your': 'secrets_from_vault'}
```

