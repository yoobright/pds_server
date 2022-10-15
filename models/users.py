import datetime

from models import db

#  argparse.Namespace to dict
def vars(args):
    return {k: v for k, v in args._get_kwargs()}

class User(db.Model):
    __tablename__ = 'user_basic_info'

    id = db.Column(db.Integer, primary_key=True)
    user_name = db.Column(db.String, nullable=False)
    uid = db.Column(db.String)
    gender = db.Column(db.String)
    age = db.Column(db.Numeric(3), nullable=False)
    height = db.Column(db.Numeric(5, 2))
    weight = db.Column(db.Numeric(5, 2))
    job = db.Column(db.String)
    edu = db.Column(db.String)
    special = db.Column(db.String, nullable=False, default="无")
    tel = db.Column(db.String)
    tumor = db.Column(db.String, nullable=False, default="无")
    tumor_metastasis = db.Column(db.String)
    tumor_treatment = db.Column(db.String)
    illness = db.Column(db.String)
    liver_function = db.Column(db.String)
    kidney_function = db.Column(db.String)
    cardiac_function = db.Column(db.String)
    allergy = db.Column(db.String)
    physical = db.Column(db.String)

    submit_time = db.Column(db.DateTime, nullable=False,
                            default=datetime.datetime.now)

    def as_dict(self):
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}

    def to_json(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email
        }
