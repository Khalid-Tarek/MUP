from datetime import date
from enum import Enum

class Type(Enum):
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