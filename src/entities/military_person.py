from datetime import date
from typing import List

class MilitaryPerson:
    def __init__(
            self, 
            military_id: int, 
            name: str, 
            start_date: date,
            telephone: List[str],
            address_governorate: str,
            address_town: str,
            address_street: str):
        self.military_id = military_id
        self.name = name
        self.start_date = start_date
        self.telephone = telephone
        self.address_governorate = address_governorate
        self.address_town = address_town
        self.address_street = address_street