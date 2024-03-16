from flask import Flask, render_template
from my_utils import HOST, PORT, BASE_LINK, UNIT_NAME
import database_utils
import atexit

app = Flask(__name__, template_folder="templates")

conn = database_utils.get_ibm_db_connection()
database_utils.check_or_create_all_tables(conn)

@app.route('/')
def hello_world():
    database_tables = database_utils.get_database_tables_as_dict(conn)

    return render_template(
        "index.html",
        BASE_LINK = BASE_LINK,
        UNIT_NAME = UNIT_NAME,
        database_tables = database_tables
    )

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True, use_reloader=False)

def exit_handler():
    print("Thank you for using Military Unit Personnel!")
    database_utils.close_ibm_db_connection(conn)
    
atexit.register(exit_handler)
    
    
