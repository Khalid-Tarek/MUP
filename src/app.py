from flask import Flask, render_template
from database_utils import *
app = Flask(__name__, template_folder="templates")

conn = get_ibm_db_connection()
check_or_create_all_tables(conn)

# Get table headers
stmt = ibm_db.exec_immediate(conn, "SELECT colname FROM syscat.columns WHERE TABNAME = 'TEST'")
soldiers_table_headers = sum(parse_db2_statement(stmt), tuple()) # I do this to flatten the 2D result list

# Get table content
stmt = ibm_db.exec_immediate(conn, "SELECT * FROM TEST")
soldiers_table_rows = parse_db2_statement(stmt)

ibm_db.close(conn)

@app.route('/')
def hello_world():
    return render_template(
        "index.html", 
        soldiers_table_headers = soldiers_table_headers, 
        soldiers_table_rows = soldiers_table_rows
    )

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)