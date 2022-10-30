# eyesonly

![test](https://github.com/diegojromerolopez/eyesonly/actions/workflows/test.yml/badge.svg)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![Maintenance](https://img.shields.io/badge/Maintained%3F-yes-green.svg)](https://github.com/diegojromerolopez/eyesonly/graphs/commit-activity)
[![made-with-python](https://img.shields.io/badge/Made%20with-Python-1f425f.svg)](https://www.python.org/)
[![Maintainability](https://api.codeclimate.com/v1/badges/aba99dc71aec83ee8787/maintainability)](https://codeclimate.com/github/diegojromerolopez/eyesonly/maintainability)
[![Test Coverage](https://api.codeclimate.com/v1/badges/aba99dc71aec83ee8787/test_coverage)](https://codeclimate.com/github/diegojromerolopez/eyesonly/test_coverage)

A package to avoid having leaks of secrets.

A proof-of concept of a way of hiding secrets by limiting the places they can be called.

IMPORTANT NOTICE: **This code is in pre-alpha stage. I am not responsible for any damage you suffer because of your use of this project.**

## Use
```python
from eyesonly.secret import Secret

# Initialize where the secrets can be used
Secret.load_allowed_uses(
            {'/whatever/path/you/like/allowed_file1.py': {'allowed_func1', 'another_func'}}
        )
```

Use the allowed function or a function called by allowed function:
```python
# This file is '/whatever/path/you/like/allowed_file1.py'
from eyesonly.secret import Secret

def allowed_func1():
    secret = Secret(name='api_key', value='SECRET_API_KEY')

    # Secret can be seen in this function 
    value = str(secret)
    assert 'SECRET_API_KEY' == value


def allowed_func2():
    secret = Secret(name='api_key', value='SECRET_API_KEY')

    # Secret can be seen in this function 
    return str(secret)
    

def another_func(self):
    # Secret can be seen in this function 
    assert 'SECRET_API_KEY' == allowed_func2()
```
