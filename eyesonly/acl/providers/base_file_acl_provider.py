import os
from typing import BinaryIO

from eyesonly.acl.acl_type import ACLType
from eyesonly.acl.providers.base_acl_provider import BaseACLProvider


class BaseFileACLProvider(BaseACLProvider):
    def __init__(self, file_path: str):
        if not os.path.isfile(file_path):
            raise ValueError(f'File {file_path} is not a valid file path')

        self._config_file_path = file_path
        self._config_dir_path = os.path.dirname(os.path.abspath(file_path))

    def _load(self, acl_config_file: BinaryIO):
        raise NotImplementedError

    def _absolutize_file_path(self, file_path: str) -> str:
        return os.path.realpath(
            os.path.join(self._config_dir_path, file_path)
        )

    def load(self) -> ACLType:
        with open(self._config_file_path, 'rb') as acl_file:
            input_config = self._load(acl_file)
        return self._input_acl_to_acl(input_acl=input_config)
