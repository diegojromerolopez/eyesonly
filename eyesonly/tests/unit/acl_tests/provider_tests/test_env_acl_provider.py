import json
import os
import unittest
from unittest.mock import patch

from eyesonly.acl.providers.env_acl_provider import EnvACLProvider


class TestEnvACLProvider(unittest.TestCase):
    def setUp(self) -> None:
        root_dir_path = os.path.dirname(os.path.abspath(__file__))
        self.resources_path = os.path.join(root_dir_path, '_resources')
        acl_json_path = os.path.join(self.resources_path, 'eyesonly.json')
        self.acl_config: str
        with open(acl_json_path, 'rb') as acl_file:
            self.acl_config: str = json.load(acl_file)

    def test_load(self):
        expected_acl = {
            'secret1': {
                '/$HOME/path/to/secret11.py': {'func1b', 'func1a'},
                '/$HOME/path/to/secret12.py': {'func2b', 'func2a'}
            },
            'secret2': {
                '/root/path/to/secret2.py': {'func4', 'func3'}
            }
        }

        acl_json = json.dumps({
            "eyesonly": {
                "secrets": [
                    {
                        "secret": "secret1",
                        "files": [
                            {
                                "file_path": "/$HOME/path/to/secret11.py",
                                "functions": [
                                    "func1b",
                                    "func1a"
                                ]
                            },
                            {
                                "file_path": "/$HOME/path/to/secret12.py",
                                "functions": ["func2b", "func2a"]
                            }
                        ]
                    },
                    {
                        "secret": "secret2",
                        "files": [
                            {
                                "file_path": "/root/path/to/secret2.py",
                                "functions": ["func4", "func3"]
                            }
                        ]
                    }
                ]
            }
        })

        with patch.dict(os.environ, {'test_acl': acl_json}, clear=True):
            acl_provider = EnvACLProvider(env_variable='test_acl')
            acl = acl_provider.load()

        self.assertEqual(expected_acl, acl)
