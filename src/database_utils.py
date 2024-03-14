# A utility module to help initiate the database

from typing import Any, List, Tuple
from ddl_queries import DDL_QUERIES
import os
os.add_dll_directory(f"{os.getcwd()}/env/Lib/site-packages/clidriver/bin/../bin")
import ibm_db
from ibm_db import IBM_DBStatement, IBM_DBConnection
from my_utils import DB2VARIABLES as DB2

connection_string = (
    f"DATABASE={DB2['database_name']};"
    f"HOSTNAME={DB2['database_hostname']};"
    f"PORT={DB2['database_port']};"
    f"PROTOCOL=TCPIP;"
    f"UID={DB2['database_username']};"
    f"PWD={DB2['database_password']};"
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
    try:
        stmt = ibm_db.exec_immediate(conn, DDL_QUERIES[name])
    except Exception as e:
        print(f"Error: {e}")
    else:
        print(f"{name} created successfully!")

# Checks the existence of all tables of the database, and attempts to create them if not found
def check_or_create_all_tables(conn: IBM_DBConnection):
    table_names = ['SOLDIER', 'TELEPHONE', 'OFFICER', 'INJURY_RECORD', 'OFFICER_SOLDIER', 'OFFICER_SOLDIER', 'REPORT']
    for table_name in table_names:
        existence_query = f"SELECT count(1) FROM SYSIBM.SYSTABLES WHERE NAME = '{table_name}' AND TYPE = 'T'"
        stmt = ibm_db.exec_immediate(conn, existence_query)
        result = parse_db2_statement(stmt)
        if result[0][0] != 1: 
            create_table(conn, table_name)

# A function that queries the database for the table with the name passed (must be all capital) and refines it for display
def get_soldiers_table(conn: IBM_DBConnection, name) -> Tuple[List[str], List[List]]:
    
    # Get table headers
    stmt = ibm_db.exec_immediate(conn, f"SELECT colname FROM syscat.columns WHERE TABNAME = '{name}' ORDER BY COLNO")
    table_headers: List[str] = sum(parse_db2_statement(stmt), tuple()) # I do this to flatten the 2D result list
    table_headers = [x.replace('_', ' ') for x in table_headers]

    # Get table content
    stmt = ibm_db.exec_immediate(conn, f"SELECT * FROM {name}")
    table_rows: List[List[Any | str]] = parse_db2_statement(stmt)
    table_rows = [[str(x).replace('_', ' ') for x in row] for row in table_rows]

    return table_headers, table_rows