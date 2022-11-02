import json
import os
from typing import BinaryIO, Dict, List

from eyesonly.acl.acl_type import ACLType
from eyesonly.acl.providers.base_acl_provider import BaseACLProvider


class EnvACLProvider(BaseACLProvider):
    def __init__(self, env_variable: str):
        self.__env_variable = env_variable
        if self.__env_variable not in os.environ:
            raise ValueError(f'Environment variable {self.__env_variable} not found')

    def load(self) -> ACLType:
        acl_config = json.loads(os.environ[self.__env_variable])

        acl = {}
        for secret_attrs in acl_config.get('eyesonly', {}).get('secrets', {}):
            secret: str = secret_attrs['secret']
            acl[secret] = {}
            for file_attrs in secret_attrs['files']:
                file_path: str = file_attrs['file_path']
                functions: List[str] = file_attrs['functions']
                acl[secret][file_path] = set(functions)
        return acl
