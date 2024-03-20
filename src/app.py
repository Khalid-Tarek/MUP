from flask import Flask, render_template, request, abort
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

    if type != 'SOLDIER' and type != 'OFFICER':
        abort(404)

    if request.method == 'POST':
        entity = {
            'MILITARY_ID': int(request.form['person_id']),
            'NAME': request.form['person_name'],
            'START_DATE': request.form['person_start_date'],
            'END_DATE': request.form['person_ed_or_yos'],
            'YEARS_OF_SERVICE': request.form['person_ed_or_yos'],
            'ROLE': request.form['person_role'],
            'GROUP_NUM': request.form['person_group_gun'],
            'GUN_NUM': request.form['person_group_gun'],
            'PRESENCE': request.form['person_presence'],
            'EDUCATION': request.form['person_education'],
            'ADDRESS_GOVERNORATE': request.form['person_address_governorate'],
            'ADDRESS_TOWN': request.form['person_address_town'],
            'ADDRESS_STREET': request.form['person_address_street'],
            'telephones': (t.strip() for t in request.form['soldier_telephones'].split(',')),
            'officer_id': int(request.form['soldier_officer'].split('.')[0].strip())
        }
        if type == 'SOLDIER':
            entity['GROUP_NUM'] = int(entity['GROUP_NUM'])
        else:
            entity['YEARS_OF_SERVICE'] = int(entity['YEARS_OF_SERVICE'])

        print(entity)
        # Pop the keys that dont correspond to the entity type
        [entity.pop(key) for key in (['GUN_NUM', 'YEARS_OF_SERVICE'] if type == 'SOLDIER' else ['END_DATE', 'GROUP_NUM', 'PRESENCE', 'EDUCATION', 'telephones', 'officer_id'])]
            
        database_utils.update_query(conn, type, entity)

    person = database_utils.select_as_dict(conn, type,'MILITARY_ID', id)[str(id)]
    associates = {}

    if(type == 'SOLDIER'):
        associates['my_officer'] = database_utils.get_soldiers_officer(conn, id)
        associates['all_officers'] = database_utils.get_table_as_dict(conn, 'OFFICER')[1]
        associates['my_telephones'] = database_utils.select_as_dict(conn, 'TELEPHONE', 'MILITARY_ID', id)
        associates['group_num_list'] = [e.value for e in soldier.GroupNum]
        associates['education_list'] = {e.name: e.value for e in soldier.EducationType}
        associates['presence_list'] = [e.name for e in soldier.PresenceState]
        associates['roles_list'] = [e.name for e in soldier.RoleType]
    else:
        associates['roles_list'] = [e.name for e in officer.RoleType]

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
    if request.method == 'POST':
        
        type = request.form['type']
        id = request.form['id']

        result = database_utils.delete_query(conn, type, database_utils.PRIMARY_KEYS[type], id)

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
    
    
