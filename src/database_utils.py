# A utility module to help initiate the database

import ddl_queries
import json
import os
os.add_dll_directory(f"{os.getcwd()}/env/Lib/site-packages/clidriver/bin/../bin")
import ibm_db
from ibm_db import IBM_DBStatement, IBM_DBConnection


def extract_credentials():
    f = open("config.json")
    db2 = json.load(f)["db2"]
    f.close()

    return db2
 
db2 = extract_credentials()

connection_string = (
    f"DATABASE={db2['database_name']};"
    f"HOSTNAME={db2['database_hostname']};"
    f"PORT={db2['database_port']};"
    f"PROTOCOL=TCPIP;"
    f"UID={db2['database_username']};"
    f"PWD={db2['database_password']};"
)

# A helper function to return a db2 connection
# Make sure to close the db connection after you're done
def get_ibm_db_connection() -> IBM_DBConnection:
    try:
        conn = ibm_db.connect(connection_string, '', '')
        print("Connection established successfully.")
    except Exception as e:
        print(f"Error: {e}")
        return None
    else:
        return conn
    
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
    query = ''
    match name:
        case 'SOLDIER':
            query = ddl_queries.SOLDIERS_TABLE
        case 'TELEPHONE':
            query = ddl_queries.TELEPHONE_TABLE
        case 'OFFICER':
            query = ddl_queries.OFFICER_TABLE
        case 'INJURY_RECORD':
            query = ddl_queries.INJURY_RECORD_TABLE
        case 'OFFICER_SOLDIER':
            query = ddl_queries.OFFICER_SOLDIER_TABLE    
            #TODO
            return
        case _:
            return
        
    try:
        stmt = ibm_db.exec_immediate(conn, query)
    except Exception as e:
        print(f"Error: {e}")
    else:
        print(f"{name} created successfully!")

# Checks the existence of all tables of the database, and attempts to create them if not found
def check_or_create_all_tables(conn: IBM_DBConnection):
    tables = ['SOLDIER', 'TELEPHONE', 'OFFICER', 'INJURY_RECORD', 'OFFICER_SOLDIER']
    for table in tables:
        existence_query = f"SELECT count(1) FROM SYSIBM.SYSTABLES WHERE NAME = '{table}' AND TYPE = 'T'"
        stmt = ibm_db.exec_immediate(conn, existence_query)
        result = parse_db2_statement(stmt)
        if result[0][0] != 1: 
            create_table(conn, table)