# A helpful module to store the DDL queries needed for creating the tables in the db

from entities.soldier import RoleType as SRT, GroupNum as GN, PresenceState as PS, EducationType as ET
from entities.officer import RoleType as ORT
from entities.injury_record import Type as T

SOLDIERS_TABLE = (
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
        f"CONSTRAINT CHK_EndAfterStart CHECK (end_date > start_date)"
    f");"
)

TELEPHONE_TABLE = (
    f"CREATE TABLE telephone( "
        f"military_id INT NOT NULL, "
        f"telephone CHAR(11) NOT NULL PRIMARY KEY, "
        f"CONSTRAINT fk_SoldierTelephone "
        f"FOREIGN KEY (military_id) "
        f"REFERENCES soldier(military_id) "
            f"ON UPDATE NO ACTION "
            f"ON DELETE CASCADE"
    f");"
)

OFFICER_TABLE = (
    f"CREATE TABLE officer( "
        f"military_id INT NOT NULL PRIMARY KEY, "
        f"name VARCHAR(50) NOT NULL, "
        f"role VARCHAR(20) NOT NULL CHECK (role IN ({ORT.as_list_of_keys_string()})), "
        f"start_date DATE NOT NULL, "
        f"years_of_service SMALLINT NOT NULL, "
        f"gun_num VARCHAR(20) NOT NULL, "
        f"address_governorate VARCHAR(20) NOT NULL, "
        f"address_town VARCHAR(20) NOT NULL, "
        f"address_street VARCHAR(30) NOT NULL, "
        f"CONSTRAINT CHK_role_values CHECK (role IN ({ORT.as_list_of_keys_string()})) "
    f");"
)

INJURY_RECORD_TABLE = (
    f"CREATE TABLE injury_record("
        f"injury_record_id INT NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1), "
        f"military_id INT NOT NULL, "
        f"date DATE NOT NULL, "
        f"type VARCHAR(20) NOT NULL, "
        f"CONSTRAINT CHK_type_values CHECK (type IN ({T.as_list_of_keys_string()})), "
        f"FOREIGN KEY (military_id) "
        f"REFERENCES soldier(military_id) "
            f"ON UPDATE NO ACTION "
            f"ON DELETE CASCADE"
    f");"
)

OFFICER_SOLDIER_TABLE = (
    #TODO
    f""
)