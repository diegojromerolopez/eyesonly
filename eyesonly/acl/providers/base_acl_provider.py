from typing import List, Dict

from eyesonly.acl.acl_type import ACLType, InputACLType


class BaseACLProvider:

    def _absolutize_file_path(self, file_path: str):
        return file_path

    def _input_acl_to_acl(self, input_acl: InputACLType) -> ACLType:
        acl = {}
        for secret_attrs in input_acl.get('eyesonly', {}).get('secrets', {}):
            secret: str = secret_attrs['secret']
            acl[secret] = {}
            for file_attrs in secret_attrs['files']:
                file_path: str = self._absolutize_file_path(file_attrs['file_path'])
                functions: List[str] = file_attrs['functions']
                acl[secret][file_path] = set(functions)
        return acl

    def load(self) -> ACLType:
        raise NotImplementedError
