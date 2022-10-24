import os
import unittest

from eyesonly.exceptions import EyesOnlyException
from eyesonly.secret import Secret


class TestSecret(unittest.TestCase):
    def setUp(self) -> None:
        self.root_path = os.path.dirname(os.path.abspath(__file__))
        Secret.clear_allowed_uses()

    def test_secret_not_allowed(self):
        secret = Secret(name='api_key', value='SECRET_API_KEY')
        with self.assertRaises(EyesOnlyException) as exc_context:
            str(secret)

        self.assertEqual('Secret api_key is not allowed to be seen here', str(exc_context.exception))

    def test_secret_allowed(self):
        Secret.load_allowed_uses(
            {os.path.join(self.root_path, 'test_secret.py'): 'test_secret_allowed'}
        )

        secret = Secret(name='api_key', value='SECRET_API_KEY')
        value = str(secret)

        self.assertEqual('SECRET_API_KEY', value)
