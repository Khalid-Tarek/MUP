from dateutil.relativedelta import relativedelta

if __name__ == "__main__":
    from military_person import *
    from printable_enum import *
else:
    from entities.military_person import *
    from entities.printable_enum import PrintableEnum


class RoleType(PrintableEnum):
    SERVICE = 1
    COMMANDER = 2
    ARTILLERY = 3
    INVESTIGATION = 4

class Officer(MilitaryPerson):
    
    @staticmethod
    def calculate_years_of_service(start_date: date) -> int:
        return relativedelta(date.today(), start_date).years

    def __init__(
            self, 
            military_id: int, 
            name: str, 
            start_date: date,
            telephone: List[str],
            address_governorate: str,
            address_town: str,
            address_street: str,
            role: RoleType,
            gun_num: str,
            years_of_service: int = -1):
        super().__init__(military_id, name, start_date, telephone, address_governorate, address_town, address_street)
        self.role = role
        self.gun_num = gun_num
        if years_of_service == -1:
            self.years_of_service = Officer.calculate_years_of_service(start_date)
        else:
            self.years_of_service = years_of_service

    def change_role(self, role: RoleType):
         self.role = role