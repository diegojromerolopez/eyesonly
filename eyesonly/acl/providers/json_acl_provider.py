import json
import os
from typing import BinaryIO, Dict

from eyesonly.acl.acl_type import ACLType
from eyesonly.acl.providers.base_file_acl_provider import BaseACLProvider


class JSONACLProvider(BaseACLProvider):
    def __init__(self, file_path: str = 'eyesonly.toml'):
        super().__init__(file_path=file_path)

    def _load(self, acl_config_file: BinaryIO) -> ACLType:
        return json.load(acl_config_file)
