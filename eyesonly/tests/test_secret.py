import json
import os
import shutil
import tempfile
import time
import unittest

from eyesonly.acl.acl import ACL
from eyesonly.acl.providers.json_acl_provider import JSONACLProvider
from eyesonly.exceptions import EyesOnlyException
from eyesonly.secret import Secret


class TestSecret(unittest.TestCase):
    def setUp(self) -> None:
        self.root_path = os.path.dirname(os.path.abspath(__file__))
        Secret.clear_allowed_uses()

        acl_config = {
            "eyesonly": {
                "secrets": [
                    {
                        "secret": "api_key",
                        "files": [
                            {
                                "file_path": os.path.join(self.root_path, 'test_secret.py'),
                                "functions": [
                                    'test_secret_allowed',
                                    'test_secret_performance',
                                    'test_allowed_in_inner_function_with_allowed_caller_function',
                                    'inner_function_in_test'
                                ]
                            }
                        ]
                    }
                ]
            }
        }
        self.temp_dir = tempfile.mkdtemp()
        self.temp_config_file_path = os.path.join(self.temp_dir, 'acl_config.json')
        with open(self.temp_config_file_path, "w") as outfile:
            json.dump(acl_config, outfile)

        acl = ACL(JSONACLProvider(file_path=self.temp_config_file_path))
        Secret.load_allowed_uses(acl=acl)

    def tearDown(self) -> None:
        shutil.rmtree(self.temp_dir)

    def test_secret_not_allowed(self):
        secret = Secret(name='api_key', value='SECRET_API_KEY')
        with self.assertRaises(EyesOnlyException) as exc_context:
            str(secret)

        self.assertEqual('Secret api_key is not allowed to be seen here', str(exc_context.exception))

    def test_secret_not_allowed_exception_denied_policy(self):
        secret = Secret(name='api_key', value='SECRET_API_KEY', denied_policy='exception')
        with self.assertRaises(EyesOnlyException) as exc_context:
            str(secret)

        self.assertEqual('Secret api_key is not allowed to be seen here', str(exc_context.exception))

    def test_secret_not_allowed_censure_denied_policy(self):
        secret = Secret(name='api_key', value='SECRET_API_KEY', denied_policy='censure')

        self.assertEqual('*****', str(secret))

    def test_secret_allowed(self):
        secret = Secret(name='api_key', value='SECRET_API_KEY')
        value = str(secret)

        self.assertEqual('SECRET_API_KEY', value)

    def test_allowed_in_inner_function_with_allowed_caller_function(self):
        def inner_function():
            secret = Secret(name='api_key', value='SECRET_API_KEY')

            return str(secret)

        self.assertEqual('SECRET_API_KEY', inner_function())

    def test_allowed_in_inner_function_with_not_allowed_caller_function(self):
        def inner_function_in_test():
            secret = Secret(name='api_key', value='SECRET_API_KEY')

            return str(secret)

        self.assertEqual('SECRET_API_KEY', inner_function_in_test())

    def test_secret_performance(self):
        secret = Secret(name='api_key', value='SECRET_API_KEY')

        dict_access_start_time = time.time()
        _ = os.environ['HOME']
        dict_access_time = time.time() - dict_access_start_time

        str_method_start_time = time.time()
        value2 = secret.str(__file__, 'test_secret_performance')
        str_method_time = time.time() - str_method_start_time

        str_cast_start_time = time.time()
        value3 = str(secret)
        str_cast_time = time.time() - str_cast_start_time

        self.assertEqual('SECRET_API_KEY', value2)
        self.assertEqual('SECRET_API_KEY', value3)
        self.assertAlmostEqual(dict_access_time, str_method_time, delta=10e-5)
        self.assertAlmostEqual(str_cast_time, str_method_time, delta=10e-2)
