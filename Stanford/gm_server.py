
from flask import Flask, abort, request, session
from flask.ext.sqlalchemy import SQLAlchemy
#from flask import abort, flash, jsonify, render_template, redirect, request, session, url_for
from credentials import DATABASE_URI, DATABASE_KEY

TEST_DELIM = '->'
SUCCESS_CODE = 'SUCCESS'
SUB_DELIM = ','

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URI
app.config['SECRET_KEY'] = DATABASE_KEY
app.debug = True
db = SQLAlchemy(app)

# Have to import after initialization
import models

@app.route('/')
def homepage():
    abort(403)

# TODO: Remove this test code
@app.route('/testDatabase', methods=['GET'])
def add_string_to_database():
    to_add = request.args.get('toAdd')
    if to_add:
        new_test = models.Test(to_add)
        new_test.save()
    in_file_name = request.args.get('file')
    if in_file_name:
        in_file = open(in_file_name, 'r')
        for line in in_file:
            name = line.strip()
            if name:
                new_test = models.Test(name)
                new_test.save()
        in_file.close()
    tests = models.Test.get_all()
    strings = [test.name for test in tests]
    return TEST_DELIM.join(strings)

@app.route('/processFile', methods=['GET'])
def process_data_file():
    file_name = request.args.get('file')
    if file_name:
        try:
            data_file = open(file_name, 'r')
            data = parse_file(data_file)
            result_str = enter_data(data)
            data_file.close()
        except IOError:
            result_str = 'IO ERROR'
        # TODO: Add exception handling for database errors
    else:
        result_str = 'NO FILE NAME PROVIDED'
    return result_str

def parse_file(in_file):
    file_contents = in_file.read()
    delim, raw_data = file_contents.split('\n')
    split_data = [data_str.lower() for data_str in raw_data.split(delim)]
    return split_data

def enter_data(data):
    name, second_name, email, contactable, subscribable, date = data[:6]
    contactable = bool(contactable)
    subscribable = bool(subscribable)
    contact = models.Contact.get_by_email(email)
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
    new_participant = models.Participant(p_map)
    new_participant.save()
    all_contacts = models.Contact.get_all()
    all_participants = models.Participant.get_all()
    all_contacts_str = '<br>'.join([con.to_string() for con in all_contacts])
    all_participants_str = '<br>'.join([par.to_string() for par in all_participants])
    return '<br>'.join([contact.to_string(), new_participant.to_string(), all_contacts_str, all_participants_str])

# Run app

if __name__ == '__main__':
    app.run(debug=True)