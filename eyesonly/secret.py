import inspect
from typing import Callable, Optional

from eyesonly.acl.acl import ACL
from eyesonly.exceptions import EyesOnlyException


class Secret:
    CENSORED_VALUE_REPLACEMENT = '*****'

    def __init__(self, name: str, value: str, acl: ACL, denied_policy: str = 'exception'):
        self.__name = name
        self.__value = value
        self.__acl = acl
        self.__denied_policy: Callable = self.__build_denied_policy(policy=denied_policy)

    def __allowed(self, file_path: str, function: str) -> bool:
        return self.__acl.allowed(secret=self.__name, file_path=file_path, function=function)

    def __str__(self):
        curr_frame = inspect.currentframe()
        finfos = inspect.getouterframes(curr_frame)
        for frame_info in finfos[1:]:
            if self.__allowed(function=frame_info.function, file_path=frame_info.filename):
                return self.__value

        return self.__denied_policy()

    def str(self, file_path: str, function: str):
        if self.__allowed(function=function, file_path=file_path):
            return self.__value

        return self.__denied_policy()

    def __build_denied_policy(self, policy: str) -> Callable:
        return getattr(self, f'_Secret__denied_policy_{policy}')

    def __denied_policy_exception(self):
        raise EyesOnlyException(f'Secret {self.__name} is not allowed to be seen here')

    def __denied_policy_censure(self):
        return self.CENSORED_VALUE_REPLACEMENT

