import os
from typing import BinaryIO, List

from eyesonly.acl.acl_type import ACLType


class BaseACLProvider:
    def __init__(self, file_path: str):
        if not os.path.isfile(file_path):
            raise ValueError(f'File {file_path} is not a valid file path')

        self._config_file_path = file_path
        self._config_dir_path = os.path.dirname(os.path.abspath(file_path))

    def _load(self, acl_config_file: BinaryIO):
        raise NotImplementedError

    def load(self) -> ACLType:
        with open(self._config_file_path, 'rb') as acl_file:
            acl_config = self._load(acl_file)

        acl = {}
        for secret_attrs in acl_config.get('eyesonly', {}).get('secrets', {}):
            secret: str = secret_attrs['secret']
            acl[secret] = {}
            for file_attrs in secret_attrs['files']:
                file_path: str = os.path.realpath(
                    os.path.join(self._config_dir_path, file_attrs['file_path'])
                )
                functions: List[str] = file_attrs['functions']
                acl[secret][file_path] = set(functions)
        return acl
