from flask import Flask, render_template
from database_utils import get_ibm_db_connection, ibm_db
app = Flask(__name__, template_folder="templates")

MUP_header = ["military_id", "name", "start_date", "end_date"]
MUP = [
    [0, "Khalid Tarek", "2/1/2023", "1/3/2024"],
    [1, "Hassan Mohammedi", "2/1/2023", "1/3/2024"],
    [2, "Alaa Fathi", "2/1/2023", "1/3/2024"],
    [3, "Basel Elsayed", "2/1/2023", "1/3/2024"],
]

conn = get_ibm_db_connection()

# Get table headers
stmt = ibm_db.exec_immediate(conn, "SELECT colname FROM syscat.columns WHERE TABNAME = 'TEST'")
try:
    print()
except:
    ibm_db.close(conn)


@app.route('/')
def hello_world():
    return render_template("index.html", MUP_header=MUP_header, MUP=MUP)

if __name__ == "__main__":
    app.run("0.0.0.0", debug=True)