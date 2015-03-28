
import os
import subprocess
import sys

from flask import Flask, abort, request, session
from flask.ext.sqlalchemy import SQLAlchemy
from credentials import DATABASE_URI, DATABASE_KEY, SCP_ARGS 

TEST_DELIM = '->'
SUB_DELIM = ','

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

@app.route('/processFile', methods=['GET'])
def process_data_file():
    file_name = request.args.get('file')
    if file_name:
        try:
            transfer_file(file_name)
            data = parse_file(file_name)
            return enter_data(data)
        except Exception as e:
            print_to_console(str(e))
            abort(ERROR_CODE)
    else:
        abort(ERROR_CODE)
    return result_str

@app.route('/viewDatabase', methods=['GET'])
def view_database():
    if app.debug:
        return get_database()
    else:
        abort(403)


# Helpers

def print_to_console(msg):
    sys.stderr.write('%s\n' % (msg))

def transfer_file(file_name):
    scp_args = list(SCP_ARGS)
    scp_args[-2] += file_name #Second to last arg is remote dir, add file name for full path
    subprocess.call(scp_args)

def parse_file(file_name):
    in_file = open(file_name, 'r')
    file_contents = in_file.read()
    #sys.stderr.write('%s\n' % (file_contents))
    delim, raw_data = file_contents.split('\n')[:2]
    split_data = [data_str.lower() for data_str in raw_data.split(delim)]
    in_file.close()
    os.remove(file_name)
    return split_data

def enter_data(data):
    name, second_name, email, contactable, subscribable, date = data[:6]
    contactable = bool(contactable)
    subscribable = bool(subscribable)
    contact = models.Contact.get_by_email(email) if email else None
    if contact:
        contact.update(name, second_name, email, contactable, subscribable, date)
    else:
        contact = models.Contact(name, second_name, email, contactable, subscribable, date)
    contact.save()
    p_map = dict()
    p_map['contact_id'] = contact.id
    p_map['birthday'] = data[6]
    p_map['gender'] = data[7]
    p_map['diagnosis'] = data[8]
    p_map['diagnosis_date'] = data[9]
    p_map['ados'] = bool(data[10])
    p_map['adir'] = bool(data[11])
    p_map['other_diagnosis_tool'] = data[12]
    p_map['city'] = data[13]
    p_map['state'] = data[14]
    p_map['country'] = data[15]
    p_map['zip_code'] = int(data[16])
    p_map['latitude'] = float(data[17])
    p_map['longitude'] = float(data[18])
    p_map['resources'] = [get_by_name(models.Resource, resource_str) for resource_str in data[19].split(SUB_DELIM)]
    p_map['related_disorders'] = [get_by_name(models.Disorder, disorder_str) for disorder_str in data[20].split(SUB_DELIM)]
    new_participant = models.Participant(p_map)
    new_participant.save()
    if app.debug:
        return get_database()
    else:
        to_return  = 'SUCCESS'
    return to_return

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