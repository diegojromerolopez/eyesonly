import json
import os
import unittest

from eyesonly.acl.acl import ACL
from eyesonly.acl.providers.env_acl_provider import EnvACLProvider
from eyesonly.acl.providers.json_acl_provider import JSONACLProvider
from eyesonly.acl.providers.toml_acl_provider import TomlACLProvider
from eyesonly.exceptions import EyesOnlyException
from eyesonly.secret import Secret


class TestSecret(unittest.TestCase):
    def setUp(self) -> None:
        root_path = os.path.dirname(os.path.abspath(__file__))
        resources_path = os.path.join(root_path, '_resources')

        json_config_file_path = os.path.join(resources_path, 'eyesonly.json')
        toml_config_file_path = os.path.join(resources_path, 'eyesonly.toml')

        os.environ['test_acl'] = json.dumps({
            "eyesonly": {
                "secrets": [
                    {
                        "secret": "env_secret1",
                        "files": [
                            {
                                "file_path": os.path.join(root_path, 'test_secret.py'),
                                "functions": [
                                    {
                                        "name": "test_env_config_secret_allowed",
                                        "inheritance": True
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        })

        self.json_acl = ACL(JSONACLProvider(file_path=json_config_file_path))
        self.env_acl = ACL(EnvACLProvider(env_variable='test_acl'))
        self.toml_acl = ACL(TomlACLProvider(file_path=toml_config_file_path))

    def test_missing_secret(self):
        secret = Secret(name='missing_secret', value='SECRET_API_KEY', acl=self.json_acl)
        with self.assertRaises(EyesOnlyException) as exc_context:
            str(secret)

        self.assertEqual('Secret missing_secret is not allowed to be seen here',
                         str(exc_context.exception))

    def test_json_config_secret_not_allowed(self):
        secret = Secret(name='secret_not_allowed_anywhere', value='SECRET_API_KEY', acl=self.json_acl)
        with self.assertRaises(EyesOnlyException) as exc_context:
            str(secret)

        self.assertEqual('Secret secret_not_allowed_anywhere is not allowed to be seen here',
                         str(exc_context.exception))

    def test_json_config_secret_not_allowed_exception_denied_policy(self):
        secret = Secret(name='secret_not_allowed_anywhere', value='SECRET_API_KEY', acl=self.json_acl,
                        denied_policy='exception')
        with self.assertRaises(EyesOnlyException) as exc_context:
            str(secret)

        self.assertEqual('Secret secret_not_allowed_anywhere is not allowed to be seen here',
                         str(exc_context.exception))

    def test_json_config_secret_not_allowed_censure_denied_policy(self):
        secret = Secret(name='secret_not_allowed_anywhere', value='SECRET_API_KEY', acl=self.json_acl,
                        denied_policy='censure')

        self.assertEqual('*****', str(secret))

    def test_json_config_secret_allowed(self):
        secret = Secret(name='secret_allowed', acl=self.json_acl, value='SECRET_API_KEY')
        value = str(secret)

        self.assertEqual('SECRET_API_KEY', value)

    def test_json_config_allowed_in_inner_function_with_allowed_caller_function(self):
        def inner_function():
            secret = Secret(name='secret_allowed', acl=self.json_acl, value='SECRET_API_KEY')

            return str(secret)

        self.assertEqual('SECRET_API_KEY', inner_function())

    def test_json_config_allowed_in_inner_function_with_not_allowed_caller_function(self):
        def inner_function_in_test():
            secret = Secret(name='secret_allowed', acl=self.json_acl, value='SECRET_API_KEY')

            return str(secret)

        self.assertEqual('SECRET_API_KEY', inner_function_in_test())

    def test_json_config_not_allowed_in_inner_function(self):
        secret = Secret(name='secret_allowed', acl=self.json_acl, value='SECRET_API_KEY')

        def inner_function_without_inheritance():
            secret_is_not_allowed_here = Secret(name='secret_allowed', acl=self.json_acl,
                                                value='SECRET_API_KEY')
            return str(secret_is_not_allowed_here)

        with self.assertRaises(EyesOnlyException) as exc_context:
            inner_function_without_inheritance()

        self.assertEqual('SECRET_API_KEY', str(secret))
        self.assertEqual('Secret secret_allowed is not allowed to be seen here',
                         str(exc_context.exception))

    def test_toml_config_secret_not_allowed(self):
        secret = Secret(name='secret_not_allowed_anywhere', value='SECRET_API_KEY', acl=self.toml_acl)
        with self.assertRaises(EyesOnlyException) as exc_context:
            str(secret)

        self.assertEqual('Secret secret_not_allowed_anywhere is not allowed to be seen here',
                         str(exc_context.exception))

    def test_toml_config_secret_allowed(self):
        secret = Secret(name='secret_allowed', acl=self.toml_acl, value='SECRET_API_KEY')
        value = str(secret)

        self.assertEqual('SECRET_API_KEY', value)

    def test_env_config_secret_not_allowed(self):
        secret = Secret(name='env_secret1', value='ENV_SECRET1', acl=self.env_acl)
        with self.assertRaises(EyesOnlyException) as exc_context:
            str(secret)

        self.assertEqual('Secret env_secret1 is not allowed to be seen here',
                         str(exc_context.exception))

    def test_env_config_secret_allowed(self):
        secret = Secret(name='env_secret1', acl=self.env_acl, value='ENV_SECRET1')
        value = str(secret)

        self.assertEqual('ENV_SECRET1', value)
