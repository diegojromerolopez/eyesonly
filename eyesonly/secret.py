import inspect
import os
from typing import List, Set, Dict

from eyesonly.exceptions import EyesOnlyException


class Secret:
    __ALLOWED_USES = {
    }

    @classmethod
    def clear_allowed_uses(cls):
        cls.__ALLOWED_USES = {}

    @classmethod
    def load_allowed_uses(cls, uses: Dict[str, Set[str]]):
        cls.__ALLOWED_USES = uses

    def __init__(self, name: str, value: str):
        self.__name = name
        self.__value = value

    def __can_see_secret(self, finfos: List[inspect.FrameInfo]):
        for frame_info in finfos[1:]:
            if frame_info.function in self.__ALLOWED_USES.get(frame_info.filename, set()):
                return True
        return False

    def __str__(self):
        curr_frame = inspect.currentframe()
        finfos = inspect.getouterframes(curr_frame)
        if not self.__can_see_secret(finfos=finfos):
            raise EyesOnlyException(f'Secret {self.__name} is not allowed to be seen here')
        return self.__value
