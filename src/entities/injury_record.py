from datetime import date

if __name__ == "__main__":
    from printable_enum import *
else:
    from entities.printable_enum import PrintableEnum

class Type(PrintableEnum):
    FRACTURE = 1
    BURN = 2
    LACERATION = 3
    MENTAL = 4
    OTHER = 5

class InjuryRecord:

    def __init__(self, military_id: int, date: date, type: Type):
        self.military_id = military_id
        self.date = date
        self.type = type