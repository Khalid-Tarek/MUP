from flask import Flask, render_template, request
from entities import officer, soldier
from my_utils import PORT, BASE_LINK, UNIT_NAME
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

    person = {}
    associates = {}
    
    if request.method == 'GET':
        person = database_utils.select_as_dict(conn, type,'MILITARY_ID', id)[str(id)]
        if(type == 'SOLDIER'):
            associates['my_officer'] = database_utils.get_soldiers_officer(conn, id)[0]
            associates['all_officers'] = database_utils.get_table_as_dict(conn, 'OFFICER')[1]
            associates['my_telephones'] = database_utils.select_as_dict(conn, 'TELEPHONE', 'MILITARY_ID', id)
            associates['group_num_list'] = [e.value for e in soldier.GroupNum]
            associates['education_list'] = {e.name: e.value for e in soldier.EducationType}
            associates['presence_list'] = [e.name for e in soldier.PresenceState]
            associates['roles_list'] = [e.name for e in soldier.RoleType]
        else:
            associates['roles_list'] = [e.name for e in officer.RoleType]
    elif request.method == 'POST':
        #TODO
        1

    return render_template(
        'edit.html',
        BASE_LINK = BASE_LINK,
        UNIT_NAME = UNIT_NAME,
        person_type = type,
        person = person,
        associates = associates
    )

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
        UNIT_NAME = UNIT_NAME,
        result = result
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True, use_reloader=True)

def exit_handler():
    print('Thank you for using Military Unit Personnel!')
    database_utils.close_ibm_db_connection(conn)
    
atexit.register(exit_handler)
    
    
