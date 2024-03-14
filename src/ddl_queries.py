# A helpful module to store the DDL queries needed for creating the tables in the db

from entities.soldier import RoleType as SRT, GroupNum as GN, PresenceState as PS, EducationType as ET
from entities.officer import RoleType as ORT
from entities.injury_record import Type as T

DDL_QUERIES = {}

DDL_QUERIES['SOLDIER'] = (
    f"CREATE TABLE soldier( "
        f"military_id INT NOT NULL PRIMARY KEY, "
        f"name VARCHAR(50) NOT NULL, "
        f"role VARCHAR(20) NOT NULL, "
        f"group_num SMALLINT NOT NULL, "
        f"presence VARCHAR(20) NOT NULL, "
        f"start_date DATE NOT NULL, "
        f"education VARCHAR(20) NOT NULL, "
        f"end_date DATE NOT NULL, "
        f"address_governorate VARCHAR(20) NOT NULL, "
        f"address_town VARCHAR(20) NOT NULL, "
        f"address_street VARCHAR(30) NOT NULL, "
        f"CONSTRAINT CHK_role_values CHECK (role IN ({SRT.as_list_of_keys_string()})), "
        f"CONSTRAINT CHK_group_num_values CHECK (group_num IN ({GN.as_list_of_values_string()})), "
        f"CONSTRAINT CHK_presence_values CHECK (presence IN ({PS.as_list_of_keys_string()})), "
        f"CONSTRAINT CHK_education_values CHECK (education IN ({ET.as_list_of_keys_string()})), "
        f"CONSTRAINT CHK_end_after_start CHECK (end_date > start_date)"
    f");"
)

DDL_QUERIES['TELEPHONE'] = (
    f"CREATE TABLE telephone( "
        f"military_id INT NOT NULL, "
        f"telephone CHAR(11) NOT NULL PRIMARY KEY, "
        f"CONSTRAINT fk_Soldier_Telephone "
        f"FOREIGN KEY (military_id) "
        f"REFERENCES soldier(military_id) "
            f"ON UPDATE NO ACTION "
            f"ON DELETE CASCADE"
    f");"
)

DDL_QUERIES['OFFICER'] = (
    f"CREATE TABLE officer( "
        f"military_id INT NOT NULL PRIMARY KEY, "
        f"name VARCHAR(50) NOT NULL, "
        f"role VARCHAR(20) NOT NULL, "
        f"start_date DATE NOT NULL, "
        f"years_of_service SMALLINT NOT NULL, "
        f"gun_num VARCHAR(20) NOT NULL, "
        f"address_governorate VARCHAR(20) NOT NULL, "
        f"address_town VARCHAR(20) NOT NULL, "
        f"address_street VARCHAR(30) NOT NULL, "
        f"CONSTRAINT CHK_role_values CHECK (role IN ({ORT.as_list_of_keys_string()})) "
    f");"
)

DDL_QUERIES['INJURY_RECORD'] = (
    f"CREATE TABLE injury_record("
        f"injury_record_id INT NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1), "
        f"military_id INT NOT NULL, "
        f"date DATE NOT NULL, "
        f"type VARCHAR(20) NOT NULL, "
        f"CONSTRAINT CHK_type_values CHECK (type IN ({T.as_list_of_keys_string()})), "
        f"CONSTRAINT fk_Soldier_InjuryRecord "
        f"FOREIGN KEY (military_id) "
        f"REFERENCES soldier(military_id) "
            f"ON UPDATE NO ACTION "
            f"ON DELETE CASCADE"
    f");"
)

DDL_QUERIES['OFFICER_SOLDIER'] = (
    f"CREATE TABLE officer_soldier("
        f"soldier_military_id INT NOT NULL PRIMARY KEY, "
        f"officer_military_id INT NOT NULL, "
        f"CONSTRAINT fk_Solider_OfficerSoldier "
        f"FOREIGN KEY (soldier_military_id) "
        f"REFERENCES soldier(military_id) "
            f"ON UPDATE NO ACTION "
            f"ON DELETE CASCADE, "
        f"CONSTRAINT fk_Officer_OfficerSoldier "
        f"FOREIGN KEY (officer_military_id) "
        f"REFERENCES officer(military_id) "
            f"ON UPDATE NO ACTION "
            f"ON DELETE CASCADE"
    f");"
)

DDL_QUERIES['REPORT'] = (
    f"CREATE TABLE report("
        f"link VARCHAR(50) NOT NULL PRIMARY KEY, "
        f"date TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP, "
        f"type VARCHAR(20) NOT NULL "
    f");"
)