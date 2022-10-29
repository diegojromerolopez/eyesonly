# eyesonly
A package to avoid having leaks of secrets.

A proof-of concept of a way of hiding secrets by limiting the places they can be called.

IMPORTANT NOTICE: **This code is in pre-alpha stage. I am not responsible for any damage you suffer because of your use of this project.**

## Use
```python
from eyesonly.secret import Secret

# Initialize where the secrets can be used
Secret.load_allowed_uses(
            {'/whatever/path/you/like/allowed_file1.py': {'allowed_func1', 'allowed_func2'}}
        )
```

Use the allowed function or a function called by allowed function:
```python
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
