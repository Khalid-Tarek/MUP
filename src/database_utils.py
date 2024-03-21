# A utility module to help initiate the database

from typing import Any, Tuple
from ddl_queries import DDL_QUERIES
import os
os.add_dll_directory(f"{os.getcwd()}/env/Lib/site-packages/clidriver/bin/../bin")
import ibm_db
from ibm_db import IBM_DBStatement, IBM_DBConnection
from my_utils import DB2VARIABLES as DB2
from entities.soldier import Soldier
from entities.officer import Officer
from entities.injury_record import InjuryRecord

connection_string = (
    f"DATABASE={DB2['database_name']};"
    f"HOSTNAME={DB2['database_hostname']};"
    f"PORT={DB2['database_port']};"
    f"PROTOCOL=TCPIP;"
    f"UID={DB2['database_username']};"
    f"PWD={DB2['database_password']};"
)
TABLE_NAMES = ['SOLDIER', 'TELEPHONE', 'OFFICER', 'INJURY_RECORD', 'OFFICER_SOLDIER', 'REPORT']
PRIMARY_KEYS = {
    'SOLDIER': 'MILITARY_ID',
    'TELEPHONE': 'TELEPHONE',
    'OFFICER': 'MILITARY_ID',
    'INJURY_RECORD': 'INJURY_RECORD_ID',
    'OFFICER_SOLDIER': 'SOLDIER_MILITARY_ID',
    'REPORT': 'LINK'
}

# A helper function to start and return a db2 connection
# Make sure to close the db connection on exit
def get_ibm_db_connection() -> IBM_DBConnection:
    try:
        conn = ibm_db.connect(connection_string, '', '')
        print(f"Connection to {DB2['database_name']} established successfully.")
    except Exception as e:
        print(f"Error: {e}")
        return None
    else:
        return conn

# A helper function to close a db2 connection
def close_ibm_db_connection(conn: IBM_DBConnection):
    ibm_db.close(conn)
    print(f"Connection to {DB2['database_name']} terminated successfully.")

# A helper function to parse the db2 statement
# returns a list of rows (which are also lists)
def parse_db2_statement(stmt: IBM_DBStatement) -> list:
    result = []

    tuple = ibm_db.fetch_tuple(stmt)
    while tuple != False:
        result.append(tuple)
        tuple = ibm_db.fetch_tuple(stmt)

    return result

# Creates the necessary table as per the name passed using the connection passed  
def create_table(conn: IBM_DBConnection, name: str):    
    try:
        stmt = ibm_db.exec_immediate(conn, DDL_QUERIES[name])
    except Exception as e:
        print(f"Error: {e}")
    else:
        print(f"{name} created successfully!")

# Checks the existence of all tables of the database, and attempts to create them if not found
def check_or_create_all_tables(conn: IBM_DBConnection):
    for table_name in TABLE_NAMES:
        existence_query = f"SELECT count(1) FROM SYSIBM.SYSTABLES WHERE NAME = '{table_name}' AND TYPE = 'T'"
        stmt = ibm_db.exec_immediate(conn, existence_query)
        result = parse_db2_statement(stmt)
        if result[0][0] != 1: 
            create_table(conn, table_name)

# Creates a dictionary of dictionaries ({military_id: {attr: value}}) of the specified entity from the SQL result. Takes a list of rows (List of Lists), and the entity name
def rows_to_dict(rows: list[list[Any | str]], entity_name: str) -> dict[str, dict[str, Any]]:
    dictionary = {}
    match entity_name:
        case 'SOLDIER':
            for row in rows: dictionary[str(row[0])] = Soldier.from_list_to_dict(row)
        case 'OFFICER':
            for row in rows: dictionary[str(row[0])] = Officer.from_list_to_dict(row)
        case 'INJURY_RECORD':
            for row in rows:
                if str(row[1]) in dictionary:
                        dictionary[str(row[1])].append(InjuryRecord.from_list_to_dict(row))
                else:
                    dictionary[str(row[1])] = [InjuryRecord.from_list_to_dict(row)]
        case 'TELEPHONE':
            for row in rows:
                if str(row[0]) in dictionary:
                    dictionary[str(row[0])].append(row[1])
                else:
                    dictionary[str(row[0])] = [row[1]]
        case 'OFFICER_SOLDIER':
            for row in rows: 
                if str(row[1]) in dictionary:
                    dictionary[str(row[1])].append(str(row[0]))
                else:
                    dictionary[str(row[1])] = [str(row[0])]
        case _:
            pass

    return dictionary
""" For case INJURY_RECORD, TELEPHONE and OFFICER_SOLDIER, their structures are different:
    
    INJURY_RECORD:      {'id0' : [injury0, injury1, .....], 'id1' : [injury0, injury1, .....], ...... }        (injury : {attr0: value0, attr1: value1, ..... })
    TELEPHONE:          {'id0': ['telephone0', 'telephone1', ..... ], 'id1': ['telephone0', 'telephone1', ..... ], ..... }
    OFFICER_SOLDIER:    {'officer_id0': ['soldier_id0', 'soldier_id1', ..... ], 'officer_id1': ['soldier_id0', 'soldier_id1', ..... ], ..... }
"""

# [DEPRECATED] Creates a dictionary of objects ({military_id: object}) of the specified entity from the SQL result. Takes a list of rows (List of Lists), and the entity name
def rows_to_object_dict(rows: list[list[Any | str]], entity_name: str) -> dict[Soldier | Officer | InjuryRecord]:
    dictionary = {}
    match entity_name:
        case 'SOLDIER':
            for row in rows: dictionary[str(row[0])] = Soldier.from_list(row)
        case 'OFFICER':
            for row in rows: dictionary[str(row[0])] = Officer.from_list(row)
        case 'INJURY_RECORD':
            for row in rows: dictionary[str(row[0])] = InjuryRecord.from_list(row)
        case _:
            pass

    return dictionary


# Queries the database for the table with the name passed (must be all capital) and returns headers and object represenations (dictionaries: {'attribute': value}) of all the rows
def get_table_as_dict(conn: IBM_DBConnection, name: str) -> Tuple[list[str], dict[str, dict[str, Any]]]:
    
    # Get table headers and replace underscores in the header names to spaces
    stmt = ibm_db.exec_immediate(conn, f"SELECT colname FROM syscat.columns WHERE TABNAME = '{name}' ORDER BY COLNO")
    table_headers: list[str] = sum(parse_db2_statement(stmt), tuple()) # I do this to flatten the 2D result list

    # Get table content and transform the lists to readablle dictionaries
    stmt = ibm_db.exec_immediate(conn, f"SELECT * FROM {name}")
    table_rows: list[list[Any | str]] = parse_db2_statement(stmt)
    table_dict: dict[str, dict[str, Any]] = rows_to_dict(table_rows, name)

    return table_headers, table_dict

# Queries the database for all the data in each of it's tables and returns a dictionary of tables (which are dictionaries themselves)
def get_database_tables_as_dict(conn: IBM_DBConnection):
    database_tables = {}

    for table_name in TABLE_NAMES:
        if table_name == 'REPORT': continue
        table = {}
        table['headers'], table['dictionaries'] = get_table_as_dict(conn, table_name)
        database_tables[table_name] = table

    return database_tables
""" Final structure for the above function:  
    database_tables = {
                       'table_0': {
                                   'headers': ['header_0', 'header_1', ......],
                                   'dictionaries': {
                                                    'id_0': {'attr_0': value_0, 'attr_1': value_1, ...... },
                                                    'id_1': {'attr_0': value_0, 'attr_1': value_1, ...... },
                                                    ......
                                                   }
                                  },
                        'table_1': { ...... },
                        ......
                       }

"""

# A join query Get the id and name of the officer this soldier is assigned to
def get_soldiers_officer(conn: IBM_DBConnection, soldier_id: int = -1):

    stmt = ibm_db.exec_immediate(conn, 
                                 f'SELECT officer.military_id, officer.name ' 
                                 f'FROM officer ' 
                                 f'INNER JOIN officer_soldier '
                                 f'ON officer.military_id = officer_soldier.officer_military_id '
                                 f'WHERE officer_soldier.soldier_military_id = {soldier_id}')

    return parse_db2_statement(stmt)

# Inserts an entity into the table with the name entity_name
def insert_query(conn: IBM_DBConnection, entity_name: str, entity: dict[str, Any]) -> Tuple[int, str]:
    
    column_names = ", ".join(entity.keys())

    # Engulf non integers in escaped quotes for sql query building
    values = ", ".join((f'{value}' if isinstance(value, int) else f'\'{value}\'') for value in entity.values())

    try:
        stmt = ibm_db.exec_immediate(conn, f'INSERT INTO {entity_name} ({column_names}) VALUES ({values})')
    except Exception as e:
        message = f"Insert Query couldn't be completed: {e}"
    else:
        rows_affected = ibm_db.num_rows(stmt)
        message = f"Insert Query completed. Number of Affected rows: {ibm_db.num_rows(stmt)}"

    return rows_affected, message

# Queries the database to select a list of columns (all by default) using the entity name, column name and the value we're looking for
# Make sure to engulf string values with escaped quotes
def select_as_dict(conn: IBM_DBStatement, entity_name: str, colname: str, where_value: str | Any, selections: list[str] = ['*']) -> dict[str, dict[str, Any]]:

    stmt = ibm_db.exec_immediate(conn, f"SELECT {', '.join(str(e) for e in selections)} FROM {entity_name} WHERE {colname} = {where_value}")
    table_rows: list[list[Any | str]] = parse_db2_statement(stmt)
    table_dict: dict[str, dict[str, Any]] = rows_to_dict(table_rows, entity_name)

    return table_dict

# Update the entitity passed through a dictionary of it's values and its entity_name (table_name)
def update_query(conn: IBM_DBConnection, entity_name: str, entity: dict[str, Any]) -> Tuple[int, str]:
    rows_affected = -1
    message = ''

    set_value_strings = ''
    
    if entity_name ==  'SOLDIER':
        # Delete all soldier telephones then insert new teleophones, then pop telephones key
        delete_query(conn, 'TELEPHONE', 'MILITARY_ID', entity['MILITARY_ID'])
        for telephone in entity['telephones']:
            insert_query(conn, 'TELEPHONE', {'MILITARY_ID': entity['MILITARY_ID'], 'TELEPHONE': telephone})
        entity.pop('telephones')

        # Delete the soldier's officer if the relationship eixsts and if it does, insert a new relationship in OFFICER_SOLDIER, then pop officer_id key
        delete_query(conn, 'OFFICER_SOLDIER', 'SOLDIER_MILITARY_ID', entity['MILITARY_ID'])
        if entity['ROLE'] == 'WITH_OFFICER' or entity['ROLE'] == 'WITH_OFFICER_DRIVER':
            insert_query(conn, 'OFFICER_SOLDIER', {'SOLDIER_MILITARY_ID' : entity['MILITARY_ID'], 'OFFICER_MILITARY_ID': entity['officer_id']})
        entity.pop('officer_id')

    # Construct the set values string from the entity columns and values
    set_value_strings = []
    for key in entity:
        value = f'{entity[key]}'
        if not isinstance(entity[key], int):
            value = f'\'{value}\''
        set_value_strings.append(f'{key} = {value}')
    set_value_final_string = ", ".join(set_value_strings)
            
    try:
        stmt = ibm_db.exec_immediate(conn, f'UPDATE {entity_name} SET {set_value_final_string} WHERE {PRIMARY_KEYS[entity_name]} = {entity[PRIMARY_KEYS[entity_name]]}')
    except Exception as e:
        message = f"Update Query couldn't be completed: {e}"
    else:
        rows_affected = ibm_db.num_rows(stmt)
        message = f"Update Query completed. Number of Affected rows: {ibm_db.num_rows(stmt)}"

    return rows_affected, message

# Deletes the records from the given entity using the passed column and value
# Make sure to engulf string values with escaped quotes
def delete_query(conn: IBM_DBConnection, entity_name: str, colname: str, value: str | Any) -> Tuple[int, str]:
    rows_affected = -1
    message = ''

    try:
        stmt = ibm_db.exec_immediate(conn, f'DELETE FROM {entity_name} WHERE {colname} = {value}')
    except Exception as e:
        message = f"Delete Query couldn't be completed: {e}"
    else:
        rows_affected = ibm_db.num_rows(stmt)
        message = f"Delete Query completed. Number of Affected rows: {ibm_db.num_rows(stmt)}"

    return rows_affected, message