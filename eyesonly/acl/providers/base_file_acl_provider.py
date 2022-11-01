import os
from typing import BinaryIO

from eyesonly.acl.acl_type import ACLType


class BaseACLProvider:
    def __init__(self, file_path: str):
        if not os.path.isfile(file_path):
            raise ValueError(f'File {file_path} is not a valid file path')

        self._file_path = file_path
        self._root_dir = os.path.dirname(os.path.abspath(file_path))

    def _load(self, acl_config_file: BinaryIO):
        raise NotImplementedError

    def load(self) -> ACLType:
        with open(self._file_path, 'rb') as acl_file:
            acl_config = self._load(acl_file)

        acl = {}
        for secret_attrs in acl_config.get('eyesonly', {}).get('secrets', {}):
            secret = secret_attrs['secret']
            acl[secret] = {}
            for file_attrs in secret_attrs['files']:
                file = file_attrs['file_path']
                functions = file_attrs['functions']
                acl[secret][file] = set(functions)
        return acl
