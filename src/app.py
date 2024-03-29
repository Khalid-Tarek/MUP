from flask import Flask, render_template, request, abort
from entities import officer, soldier, injury_record
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

@app.route('/add', methods=['POST', 'GET'])
def add_page():
    
    if request.method == 'POST':
        type = request.form['person_type']
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
            'ADDRESS_STREET': request.form['person_address_street']
        }

        if type == 'SOLDIER':
            entity['GROUP_NUM'] = int(entity['GROUP_NUM'])
        else:
            entity['YEARS_OF_SERVICE'] = int(entity['YEARS_OF_SERVICE'])

        # Pop the keys that dont correspond to the entity type
        [entity.pop(key) for key in (['GUN_NUM', 'YEARS_OF_SERVICE'] if type == 'SOLDIER' else ['END_DATE', 'GROUP_NUM', 'PRESENCE', 'EDUCATION'])]
        
        database_utils.insert_query(conn, type, entity)

        if type == 'SOLDIER':
            telephones = [telephone.strip() for telephone in request.form['soldier_telephones'].split(',')]
            for telephone in telephones:
                database_utils.insert_query(conn, 'TELEPHONE', {'MILITARY_ID': entity['MILITARY_ID'], 'TELEPHONE': telephone})
            if entity['ROLE'] == 'WITH_OFFICER' or entity['ROLE'] == 'WITH_OFFICER_DRIVER':
                my_officer_id = int(request.form['soldier_officer'].split('.')[0])
                database_utils.insert_query(conn, 'OFFICER_SOLDIER', {'SOLDIER_MILITARY_ID': entity['MILITARY_ID'], 'OFFICER_MILITARY_ID': my_officer_id})
        
    associates = {
        'all_officers': database_utils.get_table_as_dict(conn, 'OFFICER')[1],
        'group_num_list': [e.value for e in soldier.GroupNum],
        'education_list': {e.name: e.value for e in soldier.EducationType},
        'presence_list': [e.name for e in soldier.PresenceState],
        'soldiers_roles_list': [e.name for e in soldier.RoleType],
        'officers_roles_list': [e.name for e in officer.RoleType]
    }

    return render_template(
        'add.html',
        BASE_LINK = BASE_LINK,
        UNIT_NAME = UNIT_NAME,
        associates = associates
    )

@app.route('/injury', methods=['POST', 'GET'])
def injury_page():

    if request.method == 'POST':
        if request.form['action'] == 'delete':
            print(request.form['id'])
            database_utils.delete_query(conn, 'INJURY_RECORD', database_utils.PRIMARY_KEYS['INJURY_RECORD'], int(request.form['id']))
        elif request.form['action'] == 'add':
            entity = {
                'MILITARY_ID': int(request.form['injured_soldier'].split('.')[0]),
                'DATE': request.form['injury_date'],
                'TYPE': request.form['injury_type']
            }
            
            print(entity)
            database_utils.insert_query(conn, 'INJURY_RECORD', entity)
        
    all_injuries_table = {}
    all_injuries_table['headers'], all_injuries_table['dictionaries'] = database_utils.get_all_injuries_with_soldiers(conn)
    all_soldiers = database_utils.get_table_as_dict(conn, 'SOLDIER')[1]
    injury_types = [e.name for e in injury_record.Type]

    return render_template(
        'injury.html',
        BASE_LINK = BASE_LINK,
        UNIT_NAME = UNIT_NAME,
        all_injuries_table = all_injuries_table,
        all_soldiers = all_soldiers,
        injury_types = injury_types
    )

@app.route('/presence')
def presence_page():
    return render_template(
        'presence.html',
        BASE_LINK = BASE_LINK,
        UNIT_NAME = UNIT_NAME
    )

@app.route('/reports')
def reports_page():
    return render_template(
        'reports.html',
        BASE_LINK = BASE_LINK,
        UNIT_NAME = UNIT_NAME
    )

@app.route('/settings')
def settings_page():
    return render_template(
        'settings.html',
        BASE_LINK = BASE_LINK,
        UNIT_NAME = UNIT_NAME
    )

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=PORT, debug=True, use_reloader=False)

def exit_handler():
    print('Thank you for using Military Unit Personnel!')
    database_utils.close_ibm_db_connection(conn)
    
atexit.register(exit_handler)
    
    
