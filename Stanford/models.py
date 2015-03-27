
from gm_server import db

MAX_STR_LEN = 255

class Test(db.Model):

    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(MAX_STR_LEN))

    def __init__(self, test_str):
        if not test_str:
            raise Exception('Need nonempty test string')
        self.name = test_str

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

class Contact(db.Model):

    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(MAX_STR_LEN))
    second_name = db.Column(db.String(MAX_STR_LEN))
    email = db.Column(db.String(MAX_STR_LEN))
    contractable = db.Column(db.Boolean)
    subscribable = db.Column(db.Boolean)
    date = db.Column(db.Date)
    last_update = db.Column(db.DateTime)

    def __init__(name, second_name, email):
        pass

    def save(self):
        db.session.add(self)
        db.session.commit()
