# eyesonly

![test](https://github.com/diegojromerolopez/eyesonly/actions/workflows/test.yml/badge.svg)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/diegojromerolopez/eyesonly/graphs/commit-activity)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Maintainability](https://api.codeclimate.com/v1/badges/d665c0a34d0648213dd4/maintainability)](https://codeclimate.com/github/diegojromerolopez/eyesonly/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/d665c0a34d0648213dd4/test_coverage)](https://codeclimate.com/github/diegojromerolopez/eyesonly/test_coverage)

A package to avoid having leaks of secrets.

A proof-of concept of a way of hiding secrets by limiting the places they can be called.

IMPORTANT NOTICE: **This code is in pre-alpha stage. I am not responsible for any damage you suffer because of your use of this project.**

## Use

### Create a configuration file

You have to create a configuration file that specifies which secrets can be accessed from which files
and functions. This is what we call access-control-list (or ACL for short).

There are two types of configuration files that you can create: JSON and toml.

#### JSON configuration file
```json
{
  "eyesonly":{
    "secrets": [
      {
        "secret": "secret1",
        "files": [
          {
            "file_path": "../../path/to/secret11.py",
            "functions": [
              "func1b",
              "func1a"
            ]
          },
          {
            "file_path": "../../path/to/secret12.py",
            "functions": ["func2b", "func2a"]
          }
        ]
      },
      {
        "secret": "secret2",
        "files": [
          {
            "file_path": "/root/path/to/secret2.py",
            "functions": ["func4", "func3"]
          }
        ]
      }
    ]
  }
}
```

#### Toml configuration file
```toml
[eyesonly]
[[eyesonly.secrets]]
secret = 'secret1'
[[eyesonly.secrets.files]]
file_path = '../../path/to/secret11.py'
functions = [
    'func1a',
    'func1b'
]
[[eyesonly.secrets.files]]
file_path = '../../path/to/secret12.py'
functions = [
    'func2a',
    'func2b'
]

[[eyesonly.secrets]]
secret = 'secret2'
[[eyesonly.secrets.files]]
file_path = '/root/path/to/secret2.py'
functions =[
    'func3',
    'func4'
]
```

### Load your configuration file and assign the ACL to your secrets
```python
from eyesonly.secret import Secret
from eyesonly.acl.acl import ACL
from eyesonly.acl.providers.json_acl_provider import JSONACLProvider
from eyesonly.acl.providers.toml_acl_provider import TomlACLProvider

# JSON configuration file
json_acl = ACL(JSONACLProvider(file_path='path/of/your/json/config/file'))

# toml configuration file
toml_acl = ACL(TomlACLProvider(file_path='path/of/your/toml/config/file'))
```

### Declare your secrets

Declare your secrets in some __init__.py or other file in your project that
could read be used to declare your secrets (usually by reading their value from environment)

```python
# secret_depository.py
import os
from eyesonly.secret import Secret

GEO_API_SECRET = Secret(name='api_key', value=os.environ['GEO_SERVICE_API_KEY'], acl=json_acl)
DB_PASSWORD = Secret(name='postgresql_password', value=os.environ['DB_PASSWORD'], acl=json_acl)
```

Each Secret needs its own ACL, so you will have to pass it as parameter, as seen above in the
examples.

### Use your secrets in your code
```python
from .secret_depository import GEO_API_SECRET
from eyesonly.secret import Secret

assert GEO_API_SECRET.__class__ == Secret

def allowed_func1():
    # Secret can be seen in this function 
    value = str(GEO_API_SECRET)
    assert 'SECRET_API_KEY' == value


def allowed_func2():
    # Secret can be seen in this function 
    return str(GEO_API_SECRET)
    

def another_func():
    # Secret can be seen in this function 
    assert 'SECRET_API_KEY' == allowed_func2()
```
