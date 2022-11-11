from typing import Dict, Union

from eyesonly.acl.acl_type import ACLType
from eyesonly.acl.providers.base_acl_provider import BaseACLProvider


class ACL:
    INHERITANCE_BY_DEFAULT = True

    def __init__(self, provider: BaseACLProvider):
        self.__provider = provider
        self.__acl: ACLType = provider.load()

    def allowed(self, secret: str, file_path: str, function: str, function_layer: int) -> bool:
        function_attrs: Union[bool, Dict[str, str]] = self.__acl.get(secret, {}).get(file_path, {}).get(function, False)
        if not function_attrs:
            return False
        return function_layer == 1 or function_attrs.get('inheritance', self.INHERITANCE_BY_DEFAULT)
