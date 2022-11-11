# eyesonly

![test](https://github.com/diegojromerolopez/eyesonly/actions/workflows/test.yml/badge.svg)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/diegojromerolopez/eyesonly/graphs/commit-activity)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![PyPI pyversions](https://img.shields.io/pypi/pyversions/eyesonly.svg)](https://pypi.python.org/pypi/eyesonly/)
[![PyPI version eyesonly](https://badge.fury.io/py/eyesonly.svg)](https://pypi.python.org/pypi/eyesonly/)
[![PyPI status](https://img.shields.io/pypi/status/eyesonly.svg)](https://pypi.python.org/pypi/eyesonly/)
[![PyPI download month](https://img.shields.io/pypi/dm/eyesonly.svg)](https://pypi.python.org/pypi/eyesonly/)
[![Maintainability](https://api.codeclimate.com/v1/badges/d665c0a34d0648213dd4/maintainability)](https://codeclimate.com/github/diegojromerolopez/eyesonly/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/d665c0a34d0648213dd4/test_coverage)](https://codeclimate.com/github/diegojromerolopez/eyesonly/test_coverage)

<p align="center">
  <img src="https://raw.githubusercontent.com/diegojromerolopez/eyesonly/main/resources/logo.png" alt="EyesOnly Logo"/>
</p>

A package to avoid having leaks of secrets.

A way of hiding secrets by limiting the places they can be called.

IMPORTANT NOTICE: **This code is in alpha stage. Use at your own risk.**

## Use

### Create a configuration file

You have to create a configuration file that specifies which secrets can be accessed from which files
and functions. This is what we call access-control-list (or ACL for short).

The configuration file must determine the file, functions and if there is inheritance of permission grant
from the called functions if one ancestor is allowed to see the secret. By default, the inheritance is
activated (you do not have to include `"inheritance": true`, only set to false in case you do not want
inheritance).

There are three types of configuration files that you can create: JSON in file, JSON in environment variable, and toml.

#### JSON configuration file
```json
{
  "eyesonly":{
    "secrets": [
      {
        "secret": "geo_api_key",
        "files": [
          {
            "file_path": "../../secrets_use.py",
            "functions": [
              {
                "name": "allowed_use1",
                "inheritance": true
              },
              {
                "name": "allowed_use2",
                "inheritance": true
              },
              {
                "name": "allowed_use3",
                "inheritance": true
              }
            ]
          },
          {
            "file_path": "../../another_secrets_use.py",
            "functions": [
              {
                "name": "another_allowed_use1_for_it_and_all_inner_function_calls",
                "inheritance": true
              }
            ]
          }
        ]
      },
      {
        "secret": "postgresql_password",
        "files": [
          {
            "file_path": "../../secrets_use.py",
            "functions": [
              {
                "name": "allowed_use1",
                "inheritance": false
              }
            ]
          }
        ]
      }
    ]
  }
}
```

#### JSON in environment variable
Assign an environment variable with the contents of a JSON equal to the previous "JSON configuration file" section.
Note the file paths must be absolute as there is no directory to set as root.

#### Toml configuration file
```toml
[eyesonly]
[[eyesonly.secrets]]
secret = 'secret1'
[[eyesonly.secrets.files]]
file_path = '../../path/to/secret11.py'
[[eyesonly.secrets.files.functions]]
name = 'func1a'
inheritance = true
[[eyesonly.secrets.files.functions]]
name = 'func1b'
inheritance = true
[[eyesonly.secrets.files]]
file_path = '../../path/to/secret12.py'
[[eyesonly.secrets.files.functions]]
name = 'func2a'
inheritance = true
[[eyesonly.secrets.files.functions]]
name = 'func2b'
inheritance = true

[[eyesonly.secrets]]
secret = 'secret2'
[[eyesonly.secrets.files]]
file_path = '/root/path/to/secret2.py'
[[eyesonly.secrets.files.functions]]
name = 'func3'
inheritance = true
[[eyesonly.secrets.files.functions]]
name = 'func4'
inheritance = true
```

### Load your configuration file and assign the ACL to your secrets
```python
from eyesonly.secret import Secret
from eyesonly.acl.acl import ACL
from eyesonly.acl.providers.json_acl_provider import JSONACLProvider
from eyesonly.acl.providers.env_acl_provider import EnvACLProvider
from eyesonly.acl.providers.toml_acl_provider import TomlACLProvider

# JSON configuration file
json_acl = ACL(JSONACLProvider(file_path='path/of/your/json/config/file'))

# JSON in environment variable
env_acl = ACL(EnvACLProvider(env_variable='variable'))

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

GEO_API_SECRET = Secret(name='geo_api_key', value=os.environ['GEO_SERVICE_API_KEY'], acl=json_acl)
DB_PASSWORD = Secret(name='postgresql_password', value=os.environ['DB_PASSWORD'], acl=json_acl, denied_policy='censure')
```

Each Secret needs its own ACL, so you will have to pass it as parameter, as seen above in the
examples.

### Use your secrets in your code
```python
# secrets_use.py
import os
from .secret_depository import GEO_API_SECRET, DB_PASSWORD
from eyesonly.secret import Secret

assert GEO_API_SECRET.__class__ == Secret

def allowed_use1():
    # Both secrets can be seen in this function 
    assert os.environ['GEO_SERVICE_API_KEY'] == str(GEO_API_SECRET)
    assert os.environ['DB_PASSWORD'] == str(DB_PASSWORD)


def allowed_use2():
    # geo_api_key can be seen in this function 
    return str(GEO_API_SECRET)
    

def another_use3():
    # geo_api_key can be seen in this function 
    assert os.environ['GEO_SERVICE_API_KEY'] == allowed_use2()


def geo_api_key_not_allowed():
    # geo_api_key can NOT be seen in this function and will raise an exception
    return str(GEO_API_SECRET)


def postgresql_password_not_allowed():
    # postgresql_password can NOT be seen in this function but will return
    # a string with only asterisks because of the "denied_policy" parameter
    # in the Secret initializer.
    assert '*****' == str(DB_PASSWORD)
```

## License

[MIT](LICENSE), readme image is authored by me, and it is placed in the public domain.