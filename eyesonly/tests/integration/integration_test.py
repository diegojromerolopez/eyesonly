import logging
import os
import sys

from eyesonly.acl.acl import ACL
from eyesonly.acl.providers.base_acl_provider import BaseACLProvider
from eyesonly.acl.providers.json_acl_provider import JSONACLProvider
from eyesonly.acl.providers.toml_acl_provider import TomlACLProvider
from eyesonly.exceptions import EyesOnlyException
from eyesonly.secret import Secret


logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)


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


def test_secret_access(acl_provider: BaseACLProvider):
    acl_provider_name = acl_provider.__class__.__name__
    logging.info(
        msg=f'Start integration testing with provider {acl_provider_name}'
    )

    acl = ACL(provider=acl_provider)

    secret1 = Secret(name='secret1', value=os.environ['SECRET1'], acl=acl)
    secret2 = Secret(name='secret2', value=os.environ['SECRET2'], acl=acl)

    test_access_allowed_to_secret1(secret1=secret1)
    test_access_allowed_to_secret2(secret2=secret2)
    test_access_not_allowed_to_secret1(secret1=secret1)
    test_access_not_allowed_to_secret2(secret2=secret2)


def main():
    dir_path = os.path.dirname(os.path.abspath(__file__))

    json_acl_provider = JSONACLProvider(
        file_path=os.path.join(dir_path, 'eyesonly.json')
    )
    test_secret_access(acl_provider=json_acl_provider)

    toml_acl_provider = TomlACLProvider(
        file_path=os.path.join(dir_path, 'eyesonly.toml')
    )
    test_secret_access(acl_provider=toml_acl_provider)


if __name__ == '__main__':
    main()
