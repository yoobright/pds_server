from models import db


class PainAssessmentInfo(db.Model):
    __tablename__ = 'pain_assessment_info'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='主键id')
    diagnostic_id = db.Column(db.Integer, comment='关联诊断表id')
    causes = db.Column(db.String, comment='疼痛原因 0-肿瘤、1-肿瘤治疗、2-非肿瘤相关性')
    body_parts = db.Column(db.String, comment='疼痛部位 对应人体部位表 多选')
    character = db.Column(db.String, comment='疼痛性质 多选')
    level = db.Column(db.Integer, comment='疼痛强度 单选')
    aggravating_factors = db.Column(
        db.String,
        comment='疼痛加重因素 多选 0-行走、1-活动、2-体位变化、3-排便、4-咳嗽、5-进食、6-天气、7-乏力、8-精神因素')
    relief_factors = db.Column(
        db.String,
        comment='疼痛缓解因素 多选 0-服用镇痛药、1-环境安静、2-光线柔和、3-温度适宜、4-心理积极、5-家人陪伴')
    breakout_type = db.Column(
        db.String,
        comment='爆发痛类型 0-与特定活动或事件相关联、1-发生在按时给予镇痛药物的剂量间隔结束时、2-控制不佳的持续性疼痛 3-无')
    breakout_freq = db.Column(db.String, comment='爆发痛发作频率 0-<3、1-≥3')
