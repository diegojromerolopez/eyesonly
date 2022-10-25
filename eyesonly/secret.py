import inspect
from typing import Set, Dict

from eyesonly.exceptions import EyesOnlyException


class Secret:
    _ALLOWED_USES = {
    }

    @classmethod
    def clear_allowed_uses(cls):
        cls._ALLOWED_USES = {}

    @classmethod
    def load_allowed_uses(cls, uses: Dict[str, Set[str]]):
        cls._ALLOWED_USES = uses

    def __init__(self, name: str, value: str):
        self.__name = name
        self.__value = value

    def __str__(self):
        curr_frame = inspect.currentframe()
        finfos = inspect.getouterframes(curr_frame)
        for frame_info in finfos[1:]:
            if frame_info.function in self._ALLOWED_USES.get(frame_info.filename, set()):
                return self.__value

        raise EyesOnlyException(f'Secret {self.__name} is not allowed to be seen here')

    def str(self, file_path: str, function: str):
        if function in self._ALLOWED_USES.get(file_path, set()):
            return self.__value

        raise EyesOnlyException(f'Secret {self.__name} is not allowed to be seen here')

