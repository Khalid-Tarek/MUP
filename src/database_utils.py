# A utility module to help initiate the database

import ddl_queries
import json
import os
os.add_dll_directory(f"{os.getcwd()}/env/Lib/site-packages/clidriver/bin/../bin")
import ibm_db
from ibm_db import IBM_DBStatement


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
def get_ibm_db_connection():
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
def parse_db2_statement(stmt: IBM_DBStatement):
    result = []

    tuple = ibm_db.fetch_tuple(stmt)
    while tuple != False:
        result.append(tuple)
        tuple = ibm_db.fetch_tuple(stmt)

    return result

def create_table(name: str):
    #TODO
    pass

def check_all_tables_exist():
    #TODO
    pass