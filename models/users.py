import datetime

from models import db


class User(db.Model):
    __tablename__ = 'user_basic_info'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='主键id')
    user_name = db.Column(db.String, nullable=False, comment='用户名')
    uid = db.Column(db.String, comment='用户id')
    gender = db.Column(db.String, comment='性别')
    age = db.Column(db.Numeric(3), nullable=False,  comment='年龄')
    height = db.Column(db.Numeric(5, 2), comment='身高')
    weight = db.Column(db.Numeric(5, 2), comment='体重')
    job = db.Column(db.String, comment='职业')
    edu = db.Column(db.String, comment='学历')
    special = db.Column(db.String, nullable=False, default="无", comment='特殊情况')
    tel = db.Column(db.String, comment='电话')
    tumor = db.Column(db.String, nullable=False, default="无", comment='肿瘤')
    tumor_metastasis = db.Column(db.String, comment='肿瘤转移')
    tumor_treatment = db.Column(db.String, comment='肿瘤治疗')
    illness = db.Column(db.String, comment='疾病')
    liver_function = db.Column(db.String, comment='肝功能')
    kidney_function = db.Column(db.String, comment='肾功能')
    cardiac_function = db.Column(db.String, comment='心功能')
    allergy = db.Column(db.String, comment='过敏史')
    physical = db.Column(db.String, comment='身体状况')

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
