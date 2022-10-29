import os
import time
import unittest

from eyesonly.decorators import eyesonly
from eyesonly.exceptions import EyesOnlyException
from eyesonly.secret import Secret


class TestDecorators(unittest.TestCase):
    def setUp(self) -> None:
        self.root_path = os.path.dirname(os.path.abspath(__file__))
        Secret.clear_allowed_uses()
        Secret.load_allowed_uses(
            {os.path.join(self.root_path, 'test_decorators.py'): {'test_secret_type_ok', 'run_without_decorator'}}
        )

    @eyesonly
    def test_secret_type_ok(self):
        secret = Secret(name='api_key', value='SECRET_API_KEY')

        value = str(secret)
        self.assertEqual('SECRET_API_KEY', value)

    @eyesonly
    def test_secret_type_exception(self):
        secret = Secret(name='api_key', value='SECRET_API_KEY')

        with self.assertRaises(EyesOnlyException) as exc_context:
            str(secret)

        self.assertEqual('Secret api_key is not allowed to be seen here', str(exc_context.exception))

    def test_performance(self):
        @eyesonly
        def run_with_decorator():
            secret1 = Secret(name='api_key', value='SECRET_API_KEY')

            str(secret1)

        def run_without_decorator():
            secret2 = Secret(name='api_key', value='SECRET_API_KEY')

            str(secret2)

        run_without_decorator_start_time = time.time()
        run_without_decorator()
        run_without_decorator_duration = time.time() - run_without_decorator_start_time


        run_with_decorator_start_time = time.time()
        run_with_decorator()
        run_with_decorator_duration = time.time() - run_with_decorator_start_time


        self.assertLess(run_with_decorator_duration, run_without_decorator_duration)
