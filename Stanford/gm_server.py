
from flask import Flask, abort, request, session
from flask.ext.sqlalchemy import SQLAlchemy
#from flask import abort, flash, jsonify, render_template, redirect, request, session, url_for
from credentials import DATABASE_URI, DATABASE_KEY

TEST_DELIM = "->"

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

@app.route('/testDatabase', methods=['GET'])
def add_string_to_database():
    to_add = request.args.get("toAdd")
    if to_add:
        new_test = models.Test(to_add)
        new_test.save()
    in_file_name = request.args.get("file")
    if in_file_name:
        in_file = open(in_file_name, "r")
        for line in in_file:
            name = line.strip()
            if name:
                new_test = models.Test(name)
                new_test.save()
        in_file.close()
    tests = models.Test.get_all()
    strings = [test.name for test in tests]
    return TEST_DELIM.join(strings)

# Run app

if __name__ == '__main__':
    app.run(debug=True)