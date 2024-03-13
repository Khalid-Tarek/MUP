from flask import Flask, render_template
from my_utils import HOST, PORT, BASE_LINK, UNIT_NAME
import database_utils
app = Flask(__name__, template_folder="templates")

conn = database_utils.get_ibm_db_connection()
database_utils.check_or_create_all_tables(conn)

soldiers_table_headers, soldiers_table_rows = database_utils.get_soldiers_table(conn, "SOLDIER")
officers_table_headers, officers_table_rows = database_utils.get_soldiers_table(conn, 'OFFICER')

database_utils.ibm_db.close(conn)

@app.route('/')
def hello_world():
    return render_template(
        "index.html",
        BASE_LINK = BASE_LINK,
        UNIT_NAME = UNIT_NAME,
        soldiers_table_headers = soldiers_table_headers, 
        soldiers_table_rows = soldiers_table_rows,
        officers_table_headers = officers_table_headers,
        officers_table_rows = officers_table_rows
    )

if __name__ == "__main__":
    app.run(host=HOST, port=PORT, debug=True)