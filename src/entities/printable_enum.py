from enum import Enum

class PrintableEnum(Enum):
    @classmethod
    def as_list_of_values_string(cls) -> str:
        string = ""
        value_list = [e.value for e in cls]
        last_element = value_list[-1]
        for member in value_list:
            string += str(member)
            if member != last_element:
                string += ", "
        return string
    
    @classmethod
    def as_list_of_keys_string(cls) -> str:
        string = ""
        name_list = [e.name for e in cls]
        last_element = name_list[-1]
        for member in name_list:
            string += f'\'{member}\''
            if member != last_element:
                string += ", "
        return string