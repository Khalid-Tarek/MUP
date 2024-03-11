# A helpful module to store the DDL queries needed for creating the tables in the db

from entities.soldier import EducationType as ET, GroupNum as GN, RoleType as RT

SOLDIERS_TABLE = (
    f"CREATE TABLE soldier( "
        f"military_id INT NOT NULL PRIMARY KEY, "
        f"name VARCHAR(50) NOT NULL, "
        f"start_date DATE NOT NULL, "
        f"address_governorate VARCHAR(20) NOT NULL, "
        f"address_town VARCHAR(20) NOT NULL, "
        f"address_street VARCHAR(50) NOT NULL, "
        f"group_num SMALLINT NOT NULL CHECK (group_num IN ({GN.as_list_of_values_string()})), "
        f"education VARCHAR(20) NOT NULL CHECK (education IN ({ET.as_list_of_keys_string()})), "
        f"role VARCHAR(20) NOT NULL CHECK (role IN ({RT.as_list_of_keys_string()})), "
        f"end_date DATE NOT NULL CHECK (end_date > start_date), "
        f"presence SMALLINT NOT NULL CHECK (presence IN (0, 1))"
    f");"
)

TELEPHONES_TABLE = (
    f"CREATE TABLE telephones( "
        f"military_id INT NOT NULL, "
        f"telephone CHAR(11) NOT NULL, "
        f"CONSTRAINT fk_SoldierTelephone "
        f"FOREIGN KEY (military_id) "
        f"REFERENCES soldier(military_id) "
            f"ON UPDATE NO ACTION "
            f"ON DELETE CASCADE"
    f");"
)

print(TELEPHONES_TABLE)