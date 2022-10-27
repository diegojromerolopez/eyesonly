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

Use **@eyesonly** decorator for performance:
```python
from eyesonly.secret import Secret
from eyesonly.decorators import eyesonly

@eyesonly
def allowed_func1(self):
    secret = Secret(name='api_key', value='SECRET_API_KEY')

    # Secret can be seen in this function 
    value = str(secret)
    assert 'SECRET_API_KEY' == value
```
