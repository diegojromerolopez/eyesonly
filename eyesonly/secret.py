import inspect
from typing import Set, Dict, Callable

from eyesonly.exceptions import EyesOnlyException


class Secret:
    CENSORED_VALUE_REPLACEMENT = '*****'

    _ALLOWED_USES = {
    }

    @classmethod
    def clear_allowed_uses(cls):
        cls._ALLOWED_USES = {}

    @classmethod
    def load_allowed_uses(cls, uses: Dict[str, Set[str]]):
        cls._ALLOWED_USES = uses

    def __init__(self, name: str, value: str, denied_policy: str = 'exception'):
        self.__name = name
        self.__value = value
        self.__denied_policy: Callable = self.__build_denied_policy(policy=denied_policy)

    def __str__(self):
        curr_frame = inspect.currentframe()
        finfos = inspect.getouterframes(curr_frame)
        for frame_info in finfos[1:]:
            if frame_info.function in self._ALLOWED_USES.get(frame_info.filename, set()):
                return self.__value

        return self.__denied_policy()

    def str(self, file_path: str, function: str):
        if function in self._ALLOWED_USES.get(file_path, set()):
            return self.__value

        return self.__denied_policy()

    def __build_denied_policy(self, policy: str):
        return getattr(self, f'_Secret__denied_policy_{policy}')

    def __denied_policy_exception(self):
        raise EyesOnlyException(f'Secret {self.__name} is not allowed to be seen here')

    def __denied_policy_censure(self):
        return self.CENSORED_VALUE_REPLACEMENT

