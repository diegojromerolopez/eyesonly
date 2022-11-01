from typing import Union

from eyesonly.acl.acl_type import ACLType
from eyesonly.acl.providers.json_acl_provider import JSONACLProvider
from eyesonly.acl.providers.toml_acl_provider import TomlACLProvider


class ACL:
    def __init__(self, provider: Union[JSONACLProvider, TomlACLProvider]):
        self.__provider = provider
        self.__acl: ACLType = provider.load()

    def allowed(self, secret: str, file_path: str, function: str):
        return function in self.__acl.get(secret, {}).get(file_path, set())
