
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
def addStringToDatabase():
    toAdd = request.args.get("toAdd")
    if toAdd:
        new_test = models.Test(toAdd)
        new_test.save()
    inFileName = request.args.get("file")
    if inFileName:
        inFile = open(inFileName, "r")
        for line in inFile:
            name = line.strip()
            if name:
                new_test = models.Test(name)
                new_test.save()
        inFile.close()
    tests = models.Test.get_all()
    strings = [test.name for test in tests]
    return TEST_DELIM.join(strings)

# Run app

if __name__ == '__main__':
    app.run(debug=True)