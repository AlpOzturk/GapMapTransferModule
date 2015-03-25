
from info_manager import db

MAX_STR_LEN = 200

class Test(db.Model):

    __tablename__ = 'test'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(MAX_STR_LEN), index=True)

    def __init__(self, testStr):
        if not testStr:
            raise Exception('Need nonempty testString')
        self.name = testStr

    @classmethod
    def get_all(cls):
        return cls.query.all()

    def save(self):
        db.session.add(self)
        db.session.commit()