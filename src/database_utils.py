import json
import os
os.add_dll_directory(f"{os.getcwd()}/env/Lib/site-packages/clidriver/bin/../bin")
import ibm_db
import ibm_db_sa
from sqlalchemy import create_engine

f = open("config.json")
data = json.load(f)
f.close()

