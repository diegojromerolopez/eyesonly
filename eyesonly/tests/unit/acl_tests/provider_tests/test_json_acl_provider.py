import os
import unittest

from eyesonly.acl.providers.json_acl_provider import JSONACLProvider


class TestJSONACLProvider(unittest.TestCase):
    def setUp(self) -> None:
        root_dir_path = os.path.dirname(os.path.abspath(__file__))
        self.resources_path = os.path.join(root_dir_path, '_resources')

    def test_acl_file_path_does_not_exist(self):
        with self.assertRaises(ValueError) as exc_context:
            JSONACLProvider(file_path='this/file/does/not/exist.toml')

        self.assertEqual('File this/file/does/not/exist.toml is not a valid file path',
                         str(exc_context.exception))

    def test_load(self):
        expected_acl = {
            'secret1': {
                os.path.realpath(os.path.join(self.resources_path, '../../path/to/secret11.py')): {'func1b', 'func1a'},
                os.path.realpath(os.path.join(self.resources_path, '../../path/to/secret12.py')): {'func2b', 'func2a'}
            },
            'secret2': {
                '/root/path/to/secret2.py': {'func4', 'func3'}
            }
        }

        acl_provider = JSONACLProvider(file_path=os.path.join(self.resources_path, 'eyesonly.json'))
        acl = acl_provider.load()

        self.assertEqual(expected_acl, acl)
