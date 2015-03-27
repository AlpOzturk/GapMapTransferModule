
import datetime

from gm_server import db, TEST_DELIM

DATE_FORMAT = '%Y-%m-%d'
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
    contactable = db.Column(db.Boolean)
    subscribable = db.Column(db.Boolean)
    date = db.Column(db.Date)
    last_updated = db.Column(db.DateTime)

    def __init__(self, name, second_name, email, contactable, subscribable, date):
        self.update(name, second_name, email, contactable, subscribable, date)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_email(cls, email):
        return cls.query.filter(cls.email == email).first() 

    def update(self, name, second_name, email, contactable, subscribable, date):
        if name and date:
            # Mandatory: name, contactable, subscribable, date
            self.name = name
            self.second_name = second_name if second_name else None
            self.email = email if email else None
            self.contactable = contactable
            self.subscribable = subscribable
            self.date = datetime.datetime.strptime(date, DATE_FORMAT)
            self.last_updated = datetime.datetime.now()
        else:
            raise Exception('Missing mandatory field')        

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_string(self):
        to_return = [str(self.id), self.name, str(self.second_name), str(self.email), str(self.contactable), str(self.subscribable), str(self.date), str(self.last_updated)]
        return TEST_DELIM.join(to_return)

class Participant(db.Model):

    __tablename__ = 'participants'
    id = db.Column(db.Integer, primary_key=True)
    contact_id = db.Column(db.Integer, nullable=False)
    birthday = db.Column(db.Date)
    gender = db.Column(db.String(MAX_STR_LEN))
    diagnosis = db.Column(db.String(MAX_STR_LEN))
    diagnosis_date = db.Column(db.Date)
    ados = db.Column(db.Boolean)
    adir = db.Column(db.Boolean)
    other_diagnosis_tool = db.Column(db.String(MAX_STR_LEN))
    city = db.Column(db.String(MAX_STR_LEN))
    state = db.Column(db.String(MAX_STR_LEN))
    country = db.Column(db.String(MAX_STR_LEN))
    zip_code = db.Column(db.Integer)
    latitude = db.Column(db.Float)
    longitude = db.Column(db.Float)
    last_updated = db.Column(db.DateTime)

    def __init__(self, param_map):
        # Mandatory: birthday, gender, ados, adir, diagnosis, and location (city/country, latitude/longitude)
        self.contact_id = param_map['contact_id']
        self.birthday = datetime.datetime.strptime(param_map['birthday'], DATE_FORMAT)
        self.gender = param_map['gender']
        self.diagnosis = param_map['diagnosis']
        diagnosis_date_str = param_map.get('diagnosis_date', None)
        self.diagnosis_date = datetime.datetime.strptime(diagnosis_date_str, DATE_FORMAT) if diagnosis_date_str else None 
        self.ados = param_map['ados']
        self.adir = param_map['adir']
        self.other_diagnosis_tool = param_map.get('other_diagnosis_tool', None)
        self.city = param_map['city']
        self.state = param_map.get('state', None)
        self.country = param_map['country']
        self.zip_code = param_map.get('zip_code', None)
        self.latitude = param_map['latitude']
        self.longitude = param_map['longitude']
        self.last_updated = datetime.datetime.now()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()

    def to_string(self):
        to_return = [str(self.id), str(self.contact_id), str(self.birthday), self.gender, self.diagnosis, str(self.diagnosis_date), str(self.ados), str(self.adir), str(self.other_diagnosis_tool), self.city, str(self.state), self.country, str(self.zip_code), str(self.latitude), str(self.longitude), str(self.last_updated)]
        return TEST_DELIM.join(to_return)