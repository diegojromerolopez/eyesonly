from typing import Dict, Set, List, Union

# TODO: use TypedDict
InputACLType = Dict[str, Dict[str, Union[str, List[Dict[str, List[Dict[str, Union[str, List[str]]]]]]]]]
ACLType = Dict[str, Dict[str, Dict[str, Set[str]]]]
