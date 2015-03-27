
from flask import Flask, abort, request, session
from flask.ext.sqlalchemy import SQLAlchemy
#from flask import abort, flash, jsonify, render_template, redirect, request, session, url_for
from credentials import DATABASE_URI, DATABASE_KEY

TEST_DELIM = '->'
SUCCESS_CODE = 'SUCCESS'

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
    else:
        result_str = 'NO FILE NAME PROVIDED'
    return result_str

def parse_file(in_file):
    file_contents = in_file.read()
    delim, raw_data = file_contents.split('\n')
    split_data = [data_str.lower() for data_str in raw_data.split(delim)]
    return split_data

def enter_data(data):
    name, second_name, email, contactable, subscribable, date = data
    contactable = bool(contactable)
    subscribable = bool(subscribable)
    new_contact = models.Contact(name, second_name, email, contactable, subscribable, date)
    new_contact.save()
    all_contacts = models.Contact.get_all()
    all_contacts_str = '<br>'.join([contact.to_string() for contact in all_contacts])
    return 'Now added : ' + new_contact.to_string() + '<br>' + all_contacts_str

# Run app

if __name__ == '__main__':
    app.run(debug=True)