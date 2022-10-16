import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime
from sqlalchemy.orm import object_mapper

from db import db


class ModelBase(object):
    """Base class for models."""
    __table_initialized__ = False

    def save(self, session):
        """Save this object."""
        session.add(self)
        session.flush()

    def __setitem__(self, key, value):
        setattr(self, key, value)

    def __getitem__(self, key):
        return getattr(self, key)

    def __contains__(self, key):
        # Don't use hasattr() because hasattr() catches any exception, not only
        # AttributeError. We want to passthrough SQLAlchemy exceptions
        # (ex: sqlalchemy.orm.exc.DetachedInstanceError).
        try:
            getattr(self, key)
        except AttributeError:
            return False
        else:
            return True

    def get(self, key, default=None):
        return getattr(self, key, default)

    @property
    def _extra_keys(self):
        """Specifies custom fields
        Subclasses can override this property to return a list
        of custom fields that should be included in their dict
        representation.
        For reference check tests/db/sqlalchemy/test_models.py
        """
        return []

    def __iter__(self):
        columns = list(dict(object_mapper(self).columns).keys())
        # NOTE(russellb): Allow models to specify other keys that can be looked
        # up, beyond the actual db columns.  An example would be the 'name'
        # property for an Instance.
        columns.extend(self._extra_keys)

        return ModelIterator(self, iter(columns))

    def update(self, values):
        """Make the model object behave like a dict."""
        for k, v in values.items():
            setattr(self, k, v)

    def _as_dict(self):
        """Make the model object behave like a dict.
        Includes attributes from joins.
        """
        local = dict((key, value) for key, value in self)
        joined = dict([(k, v) for k, v in self.__dict__.items()
                       if not k[0] == '_'])
        local.update(joined)
        return local

    def iteritems(self):
        """Make the model object behave like a dict."""
        return self._as_dict().items()

    def items(self):
        """Make the model object behave like a dict."""
        return self._as_dict().items()

    def keys(self):
        """Make the model object behave like a dict."""
        return [key for key, value in self.iteritems()]


class ModelIterator(object):

    def __init__(self, model, columns):
        self.model = model
        self.i = columns

    def __iter__(self):
        return self

    def __next__(self):
        n = next(self.i)
        return n, getattr(self.model, n)


class User(db.Model, ModelBase):
    __tablename__ = 'user_basic_info'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='主键id')
    user_name = db.Column(db.String, nullable=False, comment='用户名')
    uid = db.Column(db.String, comment='用户id')
    gender = db.Column(db.String, nullable=False, comment='性别')
    age = db.Column(db.Numeric(3), nullable=False, comment='年龄')
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


class Diagnostic(db.Model):
    __tablename__ = 'diagnostic'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='主键id')
    patient_basic_info_id = db.Column(db.Integer, comment='关联用户基本信息表id')
    pain_assessment_info_id = db.Column(db.Integer, comment='关联疼痛评估表id')
    hist_info_id = db.Column(db.Integer, comment='关联既往用药信息id')
    decision_info_id = db.Column(db.Integer, comment='关联决策信息id')
    doctor_id = db.Column(db.Integer, comment='医师id')
    submit_time = db.Column(db.DateTime, default=datetime.datetime.now, comment='提交时间')


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


class DecisionInfo(db.Model):
    __tablename__ = 'decision_info'

    Id = db.Column(db.Integer, primary_key=True, autoincrement=True, comment='id')
    diagnostic_id = db.Column(db.Integer, comment='关联诊断表id')
    drug_table_id = db.Column(db.Integer, comment='关联用药表id')
    previous_medication_causes = db.Column(db.String, comment='既往用药存在问题及原因')
    recommendation = db.Column(db.String, comment='系统用药决策方案推荐')
    recommendation_constraint = db.Column(db.String, comment='是否取消推荐药品的约束')
    pcen_constraint = db.Column(db.String, comment='是否取消PCEN约束')
