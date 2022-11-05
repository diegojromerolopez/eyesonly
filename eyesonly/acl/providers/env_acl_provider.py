import json
import os

from eyesonly.acl.acl_type import ACLType
from eyesonly.acl.providers.base_acl_provider import BaseACLProvider


class EnvACLProvider(BaseACLProvider):
    def __init__(self, env_variable: str):
        self.__env_variable = env_variable
        if self.__env_variable not in os.environ:
            raise ValueError(f'Environment variable {self.__env_variable} not found')

    def load(self) -> ACLType:
        input_acl = json.loads(os.environ[self.__env_variable])
        return self._input_acl_to_acl(input_acl=input_acl)
