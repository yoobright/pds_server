import datetime

from models import db


class Diagnostic(db.Model):
    __tablename__ = 'diagnostic'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='主键id')
    patient_basic_info_id = db.Column(db.Integer, comment='关联用户基本信息表id')
    pain_assessment_info_id = db.Column(db.Integer, comment='关联疼痛评估表id')
    hist_info_id = db.Column(db.Integer, comment='关联既往用药信息id')
    decision_info_id = db.Column(db.Integer, comment='关联决策信息id')
    doctor_id = db.Column(db.Integer, comment='医师id')
    submit_time = db.Column(db.DateTime, default=datetime.datetime.now, comment='提交时间')


