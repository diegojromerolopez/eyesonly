import os
from typing import Dict, BinaryIO

from eyesonly.acl.acl_type import ACLType
from eyesonly.acl.providers.base_file_acl_provider import BaseACLProvider

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


class TomlACLProvider(BaseACLProvider):
    def __init__(self, file_path: str = 'eyesonly.toml'):
        super().__init__(file_path=file_path)

    def _load(self, acl_config_file: BinaryIO) -> ACLType:
        return tomllib.load(acl_config_file)
