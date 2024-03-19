from flask import Flask, render_template, request
from my_utils import HOST, PORT, BASE_LINK, UNIT_NAME
import database_utils
import atexit

app = Flask(__name__, template_folder='templates')

conn = database_utils.get_ibm_db_connection()
database_utils.check_or_create_all_tables(conn)

@app.route('/')
def index():
    database_tables = database_utils.get_database_tables_as_dict(conn)

    return render_template(
        'index.html',
        BASE_LINK = BASE_LINK,
        UNIT_NAME = UNIT_NAME,
        database_tables = database_tables
    )

@app.route('/add')
def add_page():
    #TODO
    return 1

@app.route('/injury')
def injury_page():
    #TODO
    return 1

@app.route('/presence')
def presence_page():
    #TODO
    return 1

@app.route('/reports')
def reports_page():
    #TODO
    return 1

@app.route('/settings')
def settings_page():
    #TODO
    return 1

@app.route('/edit/<type>/<int:id>', methods = ['POST', 'GET'])
def edit_page(type, id):
    #TODO
    return 1

@app.route('/delete', methods = ['POST'])
def delete_page():
    #TODO
    if request.method == 'POST':
        type = request.form['type']
        id = request.form['id']

        result = database_utils.delete_person(conn, type, id)

    return render_template(
        'delete.html',
        BASE_LINK = BASE_LINK,
        UNIT_NAME = UNIT_NAME
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True, use_reloader=True)

def exit_handler():
    print('Thank you for using Military Unit Personnel!')
    database_utils.close_ibm_db_connection(conn)
    
atexit.register(exit_handler)
    
    
