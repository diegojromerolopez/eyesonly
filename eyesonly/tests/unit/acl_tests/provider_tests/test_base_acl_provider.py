import os
import unittest

from eyesonly.acl.providers.base_file_acl_provider import BaseACLProvider


class TestBaseACLProvider(unittest.TestCase):
    def setUp(self) -> None:
        root_dir_path = os.path.dirname(os.path.abspath(__file__))
        self.resources_path = os.path.join(root_dir_path, '_resources')

    def test_load(self):
        acl_provider = BaseACLProvider(file_path=os.path.join(self.resources_path, 'eyesonly.toml'))
        with self.assertRaises(NotImplementedError):
            acl_provider.load()
