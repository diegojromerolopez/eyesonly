from typing import List, Dict

from eyesonly.acl.acl_type import ACLType, InputACLType


class BaseACLProvider:
    INHERITANCE_BY_DEFAULT = True

    def _absolutize_file_path(self, file_path: str):
        return file_path

    def _input_acl_to_acl(self, input_acl: InputACLType) -> ACLType:
        acl = {}
        for secret_attrs in input_acl.get('eyesonly', {}).get('secrets', {}):
            secret: str = secret_attrs['secret']
            acl[secret] = {}
            for file_attrs in secret_attrs['files']:
                file_path: str = self._absolutize_file_path(file_attrs['file_path'])
                acl[secret][file_path] = {}

                function_attrs_list: List[Dict[str, str]] = file_attrs['functions']
                for function_attrs in function_attrs_list:
                    if isinstance(function_attrs, str):
                        acl[secret][file_path][function_attrs] = {
                            'inheritance': self.INHERITANCE_BY_DEFAULT
                        }
                    elif isinstance(function_attrs, dict):
                        function_name = function_attrs['name']
                        acl[secret][file_path][function_name] = {
                            'inheritance': function_attrs.get('inheritance', self.INHERITANCE_BY_DEFAULT)
                        }
        return acl

    def load(self) -> ACLType:
        raise NotImplementedError
