from datetime import timedelta

if __name__ == "__main__":
    from abstract.military_person import *
    from abstract.printable_enum import PrintableEnum
    from abstract.list_dict_parsable import *
else:
    from entities.abstract.military_person import *
    from entities.abstract.printable_enum import PrintableEnum
    from entities.abstract.list_dict_parsable import *

# These are hardcoded Enumeration Classes for these fixed values used by the soldier class
# A future feature would require saving these values to the database and creating the Enums dynamically

class GroupNum(PrintableEnum):
    GROUP1 = 1
    GROUP2 = 2
    GROUP3 = 3
    
class EducationType(PrintableEnum):
    HIGHER = 424
    EXTRA_SECONDARY = 608
    SECONDARY = 789
    NONE = 1154

class RoleType(PrintableEnum):
    SERVICE = 1
    AFFAIRS = 2
    WITH_OFFICER = 3
    WITH_OFFICER_DRIVER = 4
    DRIVER = 5
    KITCHEN = 6

class PresenceState(PrintableEnum):
    VACATION = 0
    PRESENT = 1
    MISSION = 2
    SICK_LEAVE = 3
    ABSENT = 4

class Soldier(MilitaryPerson, ListDictParsable):

    @staticmethod
    def calculate_end_date(start_date: date, education: EducationType) -> date:
        return start_date + timedelta(days=education.value)
    
    def __init__(
            self, 
            military_id: int, 
            name: str, 
            role: RoleType,
            group_num: GroupNum,
            presence: PresenceState,
            start_date: date,
            education: EducationType,
            address_governorate: str,
            address_town: str,
            address_street: str,
            telephone: list[str] = [],
            end_date: date = None):
        super().__init__(military_id, name, start_date, address_governorate, address_town, address_street)
        self.telephone = telephone
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

    def add_telephone(self, nums: str | list[str]):
        self.telephone.append(nums)

    @staticmethod
    def from_list(list: list[Any]) -> Any:
        return Soldier(
            int(list[0]),
            str(list[1]),
            RoleType(getattr(RoleType, list[2])),
            GroupNum(list[3]),
            PresenceState(getattr(PresenceState, list[4])),
            datetime.strptime(str(list[5]), '%Y-%m-%d').date(),
            EducationType(getattr(EducationType, list[6])),
            str(list[8]),
            str(list[9]),
            str(list[10]),
            [],
            datetime.strptime(str(list[7]), '%Y-%m-%d').date(),
        )
    
    def to_list(self) -> list[Any]:
        return [
            self.military_id,
            self.name,
            self.role.name,
            self.group_num.value,
            self.presence.name,
            self.start_date.strftime("%Y-%m-%d"),
            self.education.name,
            self.end_date.strftime("%Y-%m-%d"),
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
            "GROUP_NUM": list[3],
            "PRESENCE": list[4],
            "START_DATE": list[5].strftime("%Y-%m-%d"),
            "EDUCATION": list[6],
            "END_DATE": list[7].strftime("%Y-%m-%d"),
            "ADDRESS_GOVERNORATE": list[8],
            "ADDRESS_TOWN": list[9],
            "ADDRESS_STREET": list[10]
        }