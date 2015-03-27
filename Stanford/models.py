
import datetime

from gm_server import db

MAX_STR_LEN = 255
DELIMITER = '\t'

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

    DATE_FORMAT = '%Y-%m-%d'

    __tablename__ = 'contacts'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(MAX_STR_LEN))
    second_name = db.Column(db.String(MAX_STR_LEN))
    email = db.Column(db.String(MAX_STR_LEN))
    contactable = db.Column(db.Boolean)
    subscribable = db.Column(db.Boolean)
    date = db.Column(db.Date)
    last_updated = db.Column(db.DateTime)

    def __init__(self, name, second_name, email, contactable, subscribable, date):
        if name and email and date:
            self.name = name
            self.second_name = second_name
            self.email = email
            self.contactable = contactable
            self.subscribable = subscribable
            self.date = datetime.datetime.strptime(date, self.DATE_FORMAT)
            self.last_updated = datetime.datetime.now()
        else:
            raise Exception('Missing mandatory field')

    @classmethod
    def get_all(cls):
        return cls.query.all() 

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_string(self):
        to_return = [self.name, str(self.second_name), self.email,str(self.contactable)]
        to_return.extend([str(self.subscribable),str(self.date),str(self.last_updated)])
        return DELIMITER.join(to_return)