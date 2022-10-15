from models import db


class DecisionInfo(db.Model):
    __tablename__ = 'decision_info'

    Id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='id')
    diagnostic_id = db.Column(db.Integer, comment='关联诊断表id')
    drug_table_id = db.Column(db.Integer, comment='关联用药表id')
    previous_medication_causes  = db.Column(db.String, comment='既往用药存在问题及原因')
    recommendation = db.Column(db.String, comment='系统用药决策方案推荐')
    recommendation_constraint = db.Column(db.String, comment='是否取消推荐药品的约束')
    pcen_constraint = db.Column(db.String, comment='是否取消PCEN约束')