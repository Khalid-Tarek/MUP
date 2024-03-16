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
            for row in rows: dictionary[str(row[0])] = InjuryRecord.from_list_to_dict(row)
        case 'TELEPHONE':
            for row in rows:
                if str(row[0]) in dictionary:
                    dictionary[str(row[0])].append(row[1])
                else:
                    dictionary[str(row[0])] = [row[1]]
        case 'OFFICER_SOLDIER':
            for row in rows: dictionary[str(row[0])] = str(row[1])
        case _:
            pass

    return dictionary

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
def get_table_as_dict(conn: IBM_DBConnection, name) -> Tuple[list[str], dict[str, dict[str, Any]]]:
    
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