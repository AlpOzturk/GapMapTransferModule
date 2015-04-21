
##### IMPORTS - CONSTANTS - INITIALIZATION #####

import sys

from datetime import datetime
from flask import Flask, abort, redirect, request, render_template, session, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from credentials import DATABASE_URI, DATABASE_KEY, IP_WHITELIST, FORM_PASSWORD, DEBUG_FLAG, NO_IP_FLAG, NO_PASS_FLAG

IP_LOG_FILE = 'ip_logs.txt'
IP_LOG_DELIMITER = '\t'

TEST_PASSWORD = 'abc123' # If changed, update in test_input.html as well
TEST_DELIM = '->'

FORM_BOOLEANS = ['contactable', 'subscribable', 'ados', 'adir']
FORM_INTEGERS = ['zip_code']
FORM_FLOATS = ['latitude', 'longitude']
FORM_MANDATORY = ['name', 'date', 'birthday', 'gender', 'diagnosis', 'city', 'country', 'latitude', 'longitude']
SUB_DELIM = ',' # Delimiter for "list" data fields for participants

ERROR_CODE = 400
FORBIDDEN_CODE = 403

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SECRET_KEY'] = DATABASE_KEY
db = SQLAlchemy(app)

app.debug = DEBUG_FLAG # DO NOT SET TO TRUE IF CONNECTED TO SENSITIVE DATABASE
app.config['NoIP'] = NO_IP_FLAG
app.config['NoPass'] = NO_PASS_FLAG
# Have to import after initialization
import models

##### MAIN ROUTING #####

@app.route('/')
def homepage():
    abort(FORBIDDEN_CODE)

@app.route('/process_data', methods=['GET', 'POST'])
def process_data():
    if ip_authorized(request):
        if request.method == 'GET':
            return redirect(url_for('test_input'))
        form = request.form
        if form:
            data_map = get_data_map(form)
            if valid_data_map(data_map):
                if password_authorized(data_map.get('password')):
                    current_contact = get_contact(data_map)
                    resource_strs = data_map.get('resources', '').split(SUB_DELIM)
                    disorder_strs = data_map.get('related_disorders', '').split(SUB_DELIM)
                    data_map['contact_id'] = current_contact.id
                    data_map['resources'] = [get_by_name(models.Resource, resource_str) for resource_str in resource_strs if resource_str]
                    data_map['related_disorders'] = [get_by_name(models.Disorder, disorder_str) for disorder_str in disorder_strs if disorder_str]
                    new_participant = models.Participant(data_map)
                    new_participant.save()
                    if app.debug:
                        return get_database()
                    else:
                        return 'SUCCESS'
                abort(FORBIDDEN_CODE)
            else:
                abort(ERROR_CODE)
        else:
            abort(ERROR_CODE)
        return result_str
    log_ip(request, 'process_data')
    abort(FORBIDDEN_CODE)

@app.route('/test_input', methods=['GET'])
def test_input():
    if ip_authorized(request):
        return render_template('test_input.html')
    log_ip(request, 'test_input')
    abort(FORBIDDEN_CODE)


@app.route('/view_database', methods=['GET'])
def view_database():
    if app.debug and ip_authorized(request):
        return get_database()
    log_ip(request, 'view_database')    
    abort(FORBIDDEN_CODE)

@app.route('/whitelist_ip', methods=['GET'])
def whitelist_ip():
    if app.debug:
        ip = get_ip(request)
        IP_WHITELIST.add(ip)
        return "Added: " + ip + ". Whitelist: " + str(IP_WHITELIST)
    log_ip(request, 'whitelist_ip') 
    abort(FORBIDDEN_CODE)

##### HELPER FUNCTIONS #####

def print_to_console(msg):
    sys.stderr.write('%s\n' % (msg))

def ip_authorized(request):
    ip = get_ip(request)
    return app.config['NoIP'] or ip in IP_WHITELIST

# Don't have write access, so only writes to console for now. Not visible through apache.
def log_ip(request, page):
    ip = get_ip(request)
    to_log = [ip, page, request.method, str(datetime.now()), '\n']
    print_to_console(IP_LOG_DELIMITER.join(to_log))

def get_ip(request):
    headers_list = request.headers.getlist("X-Forwarded-For")
    return headers_list[0] if headers_list else request.environ.get('HTTP_X_REAL_IP', request.remote_addr)

def password_authorized(password):
    correct_password = TEST_PASSWORD if app.debug else FORM_PASSWORD
    return app.config['NoPass'] or password == correct_password

def get_data_map(form):
    data_map = dict()
    for key in form:
        value = form[key].strip()
        if value:
            data_map[key] = value
    for key in FORM_BOOLEANS:
        if key in data_map:
            data_map[key] = bool(data_map[key])
        else:
            data_map[key] = False
    for key in FORM_INTEGERS:
        if key in data_map:
            data_map[key] = int(data_map[key])
    for key in FORM_FLOATS:
        if key in data_map:
            data_map[key] = float(data_map[key])
    return data_map

def valid_data_map(data_map):
    for field in FORM_MANDATORY:
        if field not in data_map:
            return False
    return True


def get_contact(data_map):
    contact = models.Contact.get_by_email(data_map.get('email', None))
    if contact:
        contact.update(data_map)
    else:
        contact = models.Contact(data_map)
    contact.save() 
    return contact

def get_by_name(target_class, name):
    instance = target_class.get_by_name(name)
    if not instance:
        instance = target_class(name)
        instance.save()
    return instance

def get_database():
    all_contacts = models.Contact.get_all()
    all_participants = models.Participant.get_all()
    all_contacts_str = '<br>'.join([con.to_string() for con in all_contacts])
    all_participants_str = '<br>'.join([par.to_string() for par in all_participants])
    to_return = '<br><br>'.join([all_contacts_str, all_participants_str, models.Resource.get_all_str(), models.Disorder.get_all_str()])
    return to_return

##### RUN APP #####

if __name__ == '__main__':
    app.run(debug=DEBUG_FLAG)
