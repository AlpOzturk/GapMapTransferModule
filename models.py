
import datetime

from gm_server import db, SUB_DELIM, TEST_DELIM

DATE_FORMAT = '%Y-%m-%d'
MAX_STR_LEN = 255

participant_resources_table = db.Table(
    'participant_resources',
    db.Column('participant_id', db.Integer, db.ForeignKey('participants.id'), primary_key=True),
    db.Column('resource_id', db.Integer, db.ForeignKey('resources.id'), primary_key=True)
)

participant_related_disorders_table = db.Table(
    'participant_related_disorders',
    db.Column('participant_id', db.Integer, db.ForeignKey('participants.id'), primary_key=True),
    db.Column('disorder_id', db.Integer, db.ForeignKey('related_disorders.id'), primary_key=True)
)


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

    def __init__(self, param_map):
        self.update(param_map)

    @classmethod
    def get_all(cls):
        return cls.query.all()

    @classmethod
    def get_by_email(cls, email):
        if email:
            return cls.query.filter(cls.email == email).first() 
        return None

    def update(self, param_map):
        # Mandatory: name, contactable, subscribable, date
        self.name = param_map['name']
        self.second_name = param_map.get('second_name', None)
        self.email = param_map.get('email', None)
        self.contactable = param_map['contactable']
        self.subscribable = param_map['subscribable']
        self.date = datetime.datetime.strptime(param_map['date'], DATE_FORMAT)
        self.last_updated = datetime.datetime.now()     

    def save(self):
        db.session.add(self)
        try_commit()

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

    participant_resources = db.relationship('Resource',
        secondary=participant_resources_table,
        lazy='dynamic',
        backref=db.backref('participant', lazy='dynamic')
    )

    participant_related_disorders = db.relationship('Disorder',
        secondary=participant_related_disorders_table,
        lazy='dynamic',
        backref=db.backref('participant', lazy='dynamic')
    )

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
        resources = param_map['resources']
        for resource in resources:
            self.participant_resources.append(resource)
        related_disorders = param_map['related_disorders']
        for disorder in related_disorders:
            self.participant_related_disorders.append(disorder)
        self.last_updated = datetime.datetime.now()

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        try_commit()

    def to_string(self):
        to_return = [str(self.id), str(self.contact_id), str(self.birthday), self.gender, self.diagnosis, str(self.diagnosis_date), str(self.ados), str(self.adir), str(self.other_diagnosis_tool), self.city, str(self.state), self.country, str(self.zip_code), str(self.latitude), str(self.longitude), str(self.last_updated)]
        to_return.append(SUB_DELIM.join([resource.resource for resource in self.participant_resources.all()]))
        to_return.append(SUB_DELIM.join([disorder.disorder for disorder in self.participant_related_disorders.all()]))
        return TEST_DELIM.join(to_return)


class Resource(db.Model):

    __tablename__ = 'resources'
    id = db.Column(db.Integer, primary_key=True)
    resource = db.Column(db.String(MAX_STR_LEN))

    def __init__(self, resource):
        self.resource = resource

    @classmethod
    def get_by_name(cls, resource):
        return cls.query.filter(cls.resource == resource).first()

    @classmethod
    def get_all_str(cls):
        all_resource_strs = [resource.resource for resource in cls.query.all()]
        return TEST_DELIM.join(all_resource_strs)

    def save(self):
        db.session.add(self)
        try_commit()


class Disorder(db.Model):

    __tablename__ = 'related_disorders'
    id = db.Column(db.Integer, primary_key=True)
    disorder = db.Column(db.String(MAX_STR_LEN))

    def __init__(self, disorder):
        self.disorder = disorder

    @classmethod
    def get_by_name(cls, disorder):
        return cls.query.filter(cls.disorder == disorder).first()

    @classmethod
    def get_all_str(cls):
        all_disorder_strs = [disorder.disorder for disorder in cls.query.all()]
        return TEST_DELIM.join(all_disorder_strs) 

    def save(self):
        db.session.add(self)
        try_commit()


# Helpers

def try_commit():
    try:
        db.session.commit()
    except:
        print 'Transaction failed'
        db.session.rollback()
        raise Exception('Failed commit')
