from enum import Enum

class PrintableEnum(Enum):
    @classmethod
    def as_list_of_values_string(cls) -> str:
        return ", ".join(str(e.value) for e in cls)
    
    @classmethod
    def as_list_of_keys_string(cls) -> str:
        return ", ".join(f"\'{e.name}\'" for e in cls)