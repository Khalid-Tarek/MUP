from dateutil.relativedelta import relativedelta

if __name__ == "__main__":
    from abstract.military_person import *
    from abstract.printable_enum import PrintableEnum
    from abstract.list_dict_parsable import *
else:
    from entities.abstract.military_person import *
    from entities.abstract.printable_enum import PrintableEnum
    from entities.abstract.list_dict_parsable import *


class RoleType(PrintableEnum):
    SERVICE = 1
    COMMANDER = 2
    ARTILLERY = 3
    INVESTIGATION = 4

class Officer(MilitaryPerson, ListDictParsable):
    
    @staticmethod
    def calculate_years_of_service(start_date: date) -> int:
        return relativedelta(date.today(), start_date).years

    def __init__(
            self, 
            military_id: int, 
            name: str, 
            role: RoleType,
            start_date: date,
            gun_num: str,
            address_governorate: str,
            address_town: str,
            address_street: str,
            years_of_service: int = -1):
        super().__init__(military_id, name, start_date, address_governorate, address_town, address_street)
        self.role = role
        self.gun_num = gun_num
        if years_of_service == -1:
            self.years_of_service = Officer.calculate_years_of_service(start_date)
        else:
            self.years_of_service = years_of_service

    def change_role(self, role: RoleType):
         self.role = role

    @staticmethod
    def from_list(list: list[Any | str]) -> Any:
        return Officer( 
            int(list[0]),
            str(list[1]),
            RoleType(getattr(RoleType, list[2])),
            datetime.strptime(str(list[3]), '%Y-%m-%d').date(),
            str(list[5]),
            str(list[6]),
            str(list[7]),
            str(list[8]),
            int(list[4])
        )
    
    def to_list(self) -> list[Any | str]:
        return [
            self.military_id,
            self.name,
            self.role.name,
            self.start_date.strftime("%Y-%m-%d"),
            self.years_of_service,
            self.gun_num,
            self.address_governorate,
            self.address_town,
            self.address_street
        ]
    
    @staticmethod
    def from_list_to_dict(list: list[Any]):
        return {
            "MILITARY_ID": list[0],
            "NAME": list[1],
            "ROLE": list[2],
            "START_DATE": list[3].strftime("%Y-%m-%d"),
            "YEARS_OF_SERVICE": list[4],
            "GUN_NUM": list[5],
            "ADDRESS_GOVERNORATE": list[6],
            "ADDRESS_TOWN": list[7],
            "ADDRESS_STREET": list[8]
        }
