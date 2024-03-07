# A utility class to help initiate the database

import json
import os
os.add_dll_directory(f"{os.getcwd()}/env/Lib/site-packages/clidriver/bin/../bin")
import ibm_db

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
