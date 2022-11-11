from typing import BinaryIO

from eyesonly.acl.acl_type import ACLType
from eyesonly.acl.providers.base_file_acl_provider import BaseFileACLProvider

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


class TomlACLProvider(BaseFileACLProvider):
    def __init__(self, file_path: str = 'eyesonly.toml'):
        super().__init__(file_path=file_path)

    def _load(self, acl_config_file: BinaryIO) -> ACLType:
        acl = tomllib.load(acl_config_file)
        return acl
