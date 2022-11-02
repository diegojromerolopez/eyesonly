import os

from eyesonly.acl.acl import ACL
from eyesonly.acl.providers.json_acl_provider import JSONACLProvider
from eyesonly.exceptions import EyesOnlyException
from eyesonly.secret import Secret


def test_access_allowed_to_secret1(secret1: Secret):
    assert 'secret1' == str(secret1)


def test_access_allowed_to_secret2(secret2: Secret):
    assert 'secret2' == str(secret2)


def test_access_not_allowed_to_secret1(secret1: Secret):
    exception = None
    try:
        str(secret1)
    except EyesOnlyException as exc:
        exception = exc

    assert 'Secret secret1 is not allowed to be seen here' == str(exception)


def test_access_not_allowed_to_secret2(secret2: Secret):
    exception = None
    try:
        str(secret2)
    except EyesOnlyException as exc:
        exception = exc

    assert 'Secret secret2 is not allowed to be seen here' == str(exception)


def main():
    dir_path = os.path.dirname(os.path.abspath(__file__))

    config_file_path = os.path.join(dir_path, 'eyesonly.json')

    acl = ACL(JSONACLProvider(file_path=config_file_path))

    secret1 = Secret(name='secret1', value=os.environ['SECRET1'], acl=acl)
    secret2 = Secret(name='secret2', value=os.environ['SECRET2'], acl=acl)

    test_access_allowed_to_secret1(secret1=secret1)
    test_access_allowed_to_secret2(secret2=secret2)
    test_access_not_allowed_to_secret1(secret1=secret1)
    test_access_not_allowed_to_secret2(secret2=secret2)


if __name__ == '__main__':
    main()
