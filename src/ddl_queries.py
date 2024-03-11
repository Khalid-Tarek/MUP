# A helpful module to store the DDL queries needed for creating the tables in the db

from entities.soldier import EducationType as ET, GroupNum as GN, RoleType as SRT
from entities.officer import RoleType as ORT
from entities.injury_record import Type as T

SOLDIERS_TABLE = (
    f"CREATE TABLE soldier( "
        f"military_id INT NOT NULL PRIMARY KEY, "
        f"name VARCHAR(50) NOT NULL, "
        f"start_date DATE NOT NULL, "
        f"address_governorate VARCHAR(20) NOT NULL, "
        f"address_town VARCHAR(20) NOT NULL, "
        f"address_street VARCHAR(30) NOT NULL, "
        f"group_num SMALLINT NOT NULL CHECK (group_num IN ({GN.as_list_of_values_string()})), "
        f"education VARCHAR(20) NOT NULL CHECK (education IN ({ET.as_list_of_keys_string()})), "
        f"role VARCHAR(20) NOT NULL CHECK (role IN ({SRT.as_list_of_keys_string()})), "
        f"end_date DATE NOT NULL, "
        f"presence SMALLINT NOT NULL CHECK (presence IN (0, 1)), "
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
        f"start_date DATE NOT NULL, "
        f"address_governorate VARCHAR(20) NOT NULL, "
        f"address_town VARCHAR(20) NOT NULL, "
        f"address_street VARCHAR(30) NOT NULL, "
        f"role VARCHAR(20) NOT NULL CHECK (role IN ({ORT.as_list_of_keys_string()})), "
        f"gun_num VARCHAR(20) NOT NULL, "
        f"years_of_service SMALLINT NOT NULL"
    f");"
)

INJURY_RECORD_TABLE = (
    f"CREATE TABLE injury_record("
        f"injury_record_id INT NOT NULL PRIMARY KEY GENERATED ALWAYS AS IDENTITY (START WITH 1 INCREMENT BY 1), "
        f"military_id INT NOT NULL, "
        f"date DATE NOT NULL, "
        f"type VARCHAR(20) NOT NULL CHECK (type IN ({T.as_list_of_keys_string()})), "
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