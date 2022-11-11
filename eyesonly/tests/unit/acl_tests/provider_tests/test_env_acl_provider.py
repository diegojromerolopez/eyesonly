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
                '/$HOME/path/to/secret11.py': {
                    'func1a': {"inheritance": True},
                    'func1b': {"inheritance": True}
                },
                '/$HOME/path/to/secret12.py': {
                    'func2a': {"inheritance": True},
                    'func2b': {"inheritance": True},
                    'func2c': {"inheritance": False}
                }
            },
            'secret2': {
                '/root/path/to/secret2.py': {
                    'func3a': {"inheritance": True},
                    'func4': {"inheritance": True}
                }
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
                                    {
                                        "name": "func1a"
                                    },
                                    {
                                        "name": "func1b",
                                        "inheritance": True
                                    }
                                ]
                            },
                            {
                                "file_path": "/$HOME/path/to/secret12.py",
                                "functions": [
                                    {
                                        "name": "func2a"
                                    },
                                    {
                                        "name": "func2b",
                                        "inheritance": True
                                    },
                                    {
                                        "name": "func2c",
                                        "inheritance": False
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "secret": "secret2",
                        "files": [
                            {
                                "file_path": "/root/path/to/secret2.py",
                                "functions": [
                                    {
                                        "name": "func4"
                                    },
                                    {
                                        "name": "func3a",
                                        "inheritance": True
                                    }
                                ]
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
