# A utility module to load the project variables from config.json file

import json

def extract_project_variables():
    f = open("config.json")
    config_variables = json.load(f)
    f.close()

    return config_variables
 
pv = extract_project_variables()

DB2VARIABLES = pv["db2"]

HOST = pv["host"]
PORT = pv["port"]
BASE_LINK = f"http://{HOST}:{PORT}"

UNIT_NAME = pv["unit_name"]