from flask import Flask, render_template
from my_utils import HOST, PORT, BASE_LINK, UNIT_NAME
import database_utils
import atexit

app = Flask(__name__, template_folder="templates")

conn = database_utils.get_ibm_db_connection()
database_utils.check_or_create_all_tables(conn)

@app.route('/')
def hello_world():
    soldiers_table, officers_table, injury_records_table = {}, {}, {}
    soldiers_table['headers'], soldiers_table['dictionaries'] = database_utils.get_table(conn, 'SOLDIER')
    officers_table['headers'], officers_table['dictionaries'] = database_utils.get_table(conn, 'OFFICER')
    injury_records_table['headers'], injury_records_table['dictionaries'] = database_utils.get_table(conn, 'INJURY_RECORD')

    return render_template(
        "index.html",
        BASE_LINK = BASE_LINK,
        UNIT_NAME = UNIT_NAME,
        soldiers_table = soldiers_table,
        officers_table = officers_table,
        injury_records_table = injury_records_table
    )

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True, use_reloader=False)

def exit_handler():
    print("Thank you for using Military Unit Personnel!")
    database_utils.close_ibm_db_connection(conn)
    
atexit.register(exit_handler)
    
    
