from datetime import timedelta

if __name__ == "__main__":
    from military_person import *
    from printable_enum import *
else:
    from entities.military_person import *
    from entities.printable_enum import PrintableEnum

class GroupNum(PrintableEnum):
    GROUP1 = 1
    GROUP2 = 2
    GROUP3 = 3
    
class EducationType(PrintableEnum):
    HIGHER = 424
    EXTRA_SECONDARY = 604
    SECONDARY = 789
    NONE = 1154

class RoleType(PrintableEnum):
    SERVICE = 1
    AFFAIRS = 2
    OFFICE = 3
    DRIVER = 4
    KITCHEN = 5

class Soldier(MilitaryPerson):

    @staticmethod
    def calculate_end_date(start_date: date, education: EducationType) -> date:
        return start_date + timedelta(days=education.value)
    
    def __init__(
            self, 
            military_id: int, 
            name: str, 
            start_date: date,
            telephone: List[str],
            address_governorate: str,
            address_town: str,
            address_street: str,
            group_num: GroupNum,
            education: EducationType,
            role: RoleType,
            end_date: date = None,
            presence: bool = True):
        super().__init__(military_id, name, start_date, telephone, address_governorate, address_town, address_street)
        self.group_num = group_num
        self.education = education
        self.role = role

        if end_date == None:
            self.end_date = Soldier.calculate_end_date(start_date, education)
        else: 
            self.end_date = end_date

        self.presence = presence

    def change_group(self, group: GroupNum):
        self.group = group

    def change_role(self, role: RoleType):
         self.role = role