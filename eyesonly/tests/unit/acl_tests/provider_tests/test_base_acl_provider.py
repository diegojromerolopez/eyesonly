import unittest

from eyesonly.acl.providers.base_acl_provider import BaseACLProvider


class TestBaseACLProvider(unittest.TestCase):
    def test_load(self):
        acl_provider = BaseACLProvider()
        with self.assertRaises(NotImplementedError):
            acl_provider.load()
