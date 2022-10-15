from models import db


class PreviousMedicationInfo(db.Model):
    __tablename__ = 'previous_medication_info'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='主键id')
    diagnostic_id = db.Column(db.Integer, comment='关联诊断表id')
    forget = db.Column(db.String, comment='是否忘记用药 0-是 ，1-否')
    carelessly = db.Column(db.String, comment='是否不注意用药 0-是 ，1-否')
    withdrawal = db.Column(db.String, comment='是否自行停药 0-是 ，1-否')
    bad_withdrawal = db.Column(db.String, comment='症状更糟时是否曾停止服药 0-是 ，1-否')
    adverse_reaction = db.Column(db.String, comment='不良反应 1 无 2便秘 3恶心呕吐4 谵妄 5过度镇静6 皮肤瘙痒7 呼吸抑制 8其他')
    adverse_reaction_drugs = db.Column(db.String, comment='不良反应用药')
    drug_table_id = db.Column(db.Integer, comment='用药表id')

