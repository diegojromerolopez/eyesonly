from eyesonly.acl.acl_type import ACLType


class BaseACLProvider:

    def load(self) -> ACLType:
        raise NotImplementedError
