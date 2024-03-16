from datetime import date, datetime

if __name__ == "__main__":
    from abstract.printable_enum import PrintableEnum
    from abstract.list_dict_parsable import *
else:
    from entities.abstract.printable_enum import PrintableEnum
    from entities.abstract.list_dict_parsable import *

class Type(PrintableEnum):
    FRACTURE = 1
    BURN = 2
    LACERATION = 3
    MENTAL = 4
    OTHER = 5

class InjuryRecord(ListDictParsable):

    def __init__(self, injury_record_id: int, military_id: int, date: date, type: Type):
        self.injury_record_id = injury_record_id
        self.military_id = military_id
        self.date = date
        self.type = type
    
    @staticmethod
    def from_list(list: list[Any | str]) -> Any:
        return InjuryRecord(
            int(list[0]),
            int(list[1]),
            datetime.strptime(str(list[2]), '%Y-%m-%d').date(),
            Type(getattr(Type, list[3]))
        )

    def to_list(self) -> list[Any | str]:
        return [
            self.injury_record_id,
            self.military_id,
            self.date.strftime("%Y-%m-%d"),
            self.type.name
        ]
    
    @staticmethod
    def from_list_to_dict(list: list[Any]):
        return {
            'INJURY_RECORD_ID': list[0],
            'MILITARY_ID': list[1],
            'DATE': list[2].strftime("%Y-%m-%d"),
            'TYPE': list[3]
        }