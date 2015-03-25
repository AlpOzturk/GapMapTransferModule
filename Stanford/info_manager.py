
from flask import Flask
from credentials import DATABASE_URI, DATABASE_KEY

app = Flask(__name__)
app.config['DATABASE_URI'] = DATABASE_URI
app.config['DATABASE_KEY'] = DATABASE_KEY
app.debug = True

@app.route('/')
def homepage():
    return "Under construction"

# Run app

if __name__ == '__main__':
    app.run(debug=True)