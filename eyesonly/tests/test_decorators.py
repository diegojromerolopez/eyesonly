import os
import unittest

from eyesonly.decorators import eyesonly
from eyesonly.exceptions import EyesOnlyException
from eyesonly.secret import Secret


class TestDecorators(unittest.TestCase):
    def setUp(self) -> None:
        self.root_path = os.path.dirname(os.path.abspath(__file__))
        Secret.clear_allowed_uses()

    @eyesonly
    def test_secret_type_ok(self):
        Secret.load_allowed_uses(
            {os.path.join(self.root_path, 'test_decorators.py'): 'test_secret_type_ok'}
        )
        secret = Secret(name='api_key', value='SECRET_API_KEY')

        value = str(secret)
        self.assertEqual('SECRET_API_KEY', value)

    @eyesonly
    def test_secret_type_exception(self):
        Secret.load_allowed_uses(
            {os.path.join(self.root_path, 'test_decorators.py'): 'test_secret_type_ok'}
        )
        secret = Secret(name='api_key', value='SECRET_API_KEY')

        with self.assertRaises(EyesOnlyException) as exc_context:
            str(secret)

        self.assertEqual('Secret api_key is not allowed to be seen here', str(exc_context.exception))
