from typing import Any


class ListDictParsable:
    
    # [DEPRECATED: use from_list_to_dict(list)] Created to help parse objects through lists
    @staticmethod
    def from_list(list: list[Any | str]) -> Any:
        pass

    # [DEPRECATED] Created to help translate objects to lists
    def to_list(self) -> list[Any | str]:
        pass

    @staticmethod
    def from_list_to_dict(list: list[Any | str]) -> dict[Any]:
        pass