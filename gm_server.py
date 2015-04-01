
import os
import subprocess
import sys

from flask import Flask, abort, redirect, request, render_template, session, url_for
from flask.ext.sqlalchemy import SQLAlchemy
from credentials import DATABASE_URI, DATABASE_KEY

TEST_DELIM = '->'
SUB_DELIM = ','

FORM_BOOLEANS = ['contactable', 'subscribable', 'ados', 'adir']
FORM_INTEGERS = ['zip_code']
FORM_FLOATS = ['latitude', 'longitude']

ERROR_CODE = 400

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SECRET_KEY'] = DATABASE_KEY
db = SQLAlchemy(app)

# Have to import after initialization
import models

@app.route('/')
def homepage():
    abort(403)

@app.route('/process_data', methods=['GET', 'POST'])
def process_data():
    if request.method == 'GET':
        return redirect(url_for('test_input'))
    form = request.form
    if form:
        data_map = get_data_map(form)
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
    else:
        abort(ERROR_CODE)
    return result_str

@app.route('/test_input', methods=['GET'])
def test_input():
    return render_template('test_input.html')


@app.route('/view_database', methods=['GET'])
def view_database():
    if app.debug:
        return get_database()
    else:
        abort(403)


# Helpers

def print_to_console(msg):
    sys.stderr.write('%s\n' % (msg))

def get_data_map(form):
    data_map = dict()
    for key in form:
        value = form[key].strip()
        if value or value:
            data_map[key] = value
    # TODO: Rm duplicated code, decompose and use lambdas?
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

# Run app

if __name__ == '__main__':
    app.run(debug=True)