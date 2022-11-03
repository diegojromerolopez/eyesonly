import json
from typing import BinaryIO

from eyesonly.acl.acl_type import ACLType
from eyesonly.acl.providers.base_file_acl_provider import BaseFileACLProvider


class JSONACLProvider(BaseFileACLProvider):
    def __init__(self, file_path: str = 'eyesonly.json'):
        super().__init__(file_path=file_path)

    def _load(self, acl_config_file: BinaryIO) -> ACLType:
        return json.load(acl_config_file)
