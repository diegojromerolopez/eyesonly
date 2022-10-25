from functools import wraps

from eyesonly.secret import Secret


def eyesonly(func):
    @wraps(func)
    def wrap(*args, **kwargs):
        func.__globals__['Secret'] = __build_secret_class(
            'Secret', func.__globals__['__file__'], func.__name__
        )
        return func(*args, **kwargs)
    return wrap


def __build_secret_class(class_name: str, file_path: str, function: str):
    return type(class_name, (Secret,), {
        '__str__': lambda s: Secret.str(s, file_path, function)
    })