## ABConfig

#### Install

```bash
pip install abconfig
```

#### Example:

```python
from abconfig import ABConfig

class DBConf(ABConfig):
	path 
    redis = '127.0.0.1:6379'
    postgres = dict(
		user='db_user',
        password='db_password'
        host='localhost',
        port='5432',
    )
```

This class will be read file:

##### Json

```json
{ 
    "redis": "172.17.0.1:6379",
    "postgres": {
		"user": "db_user",
        "password": "db_password",
        "host": "172.17.0.1",
        "port": "5432"
    }
}
```

or

##### Yaml 

```yaml
redis: "172.17.0.1:6379"
postgres:
  user: "db_user"
  password: "db_password"
  host: "172.17.0.1"
  port: "5432"
```

Create instance and use ```.get()``` or ```.get(key, default)```

```python
>> conf = DBConf()
>> conf.get()
{'redis': '172.17.0.1:6379', 'postgres': {'user': 'db_user', 'password': 'db_password', 'host': '172.17.0.1', 'port': '5432'}}
>> conf.get('redis')
172.17.0.1:6379
>> conf['postgres']['user']
db_user
```

**To override** value with environment variables, add them to os env in uppercase:

```bash
REDIS="172.17.0.3:6379"
POSTGRES_HOST="172.17.0.3"
POSTGRES_PORT="5432"
```

and create new class instance

```python
>> conf = DBConf()
>> conf.get()
{'redis': '172.17.0.3:6379', 'postgres': {'user': 'db_user', 'password': 'db_password', 'host': '172.17.0.3', 'port': '5432'}}
```

