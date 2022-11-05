from eyesonly.acl.acl_type import ACLType
from eyesonly.acl.providers.base_acl_provider import BaseACLProvider


class ACL:
    def __init__(self, provider: BaseACLProvider):
        self.__provider = provider
        self.__acl: ACLType = provider.load()

    def allowed(self, secret: str, file_path: str, function: str):
        return function in self.__acl.get(secret, {}).get(file_path, set())
