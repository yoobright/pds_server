import datetime

from sqlalchemy import Column
from sqlalchemy import DateTime, Integer, String, Float, Boolean
from sqlalchemy.orm import deferred
from sqlalchemy.orm import object_mapper, relationship

from db import DB_Obj

DB = DB_Obj.db


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


class TimestampMixin(object):
    created_at = Column(DateTime, default=datetime.datetime.now)
    updated_at = Column(DateTime, onupdate=datetime.datetime.now)


class AppBase(ModelBase, TimestampMixin):
    deleted_at = Column(DateTime)
    deleted = Column(Boolean, default=False)
    metadata = None

    @staticmethod
    def delete_values():
        return {'deleted': True, 'deleted_at': datetime.datetime.now()}

    def delete(self, session):
        """Delete this object."""
        updated_values = self.delete_values()
        updated_values['updated_at'] = self.updated_at
        self.update(updated_values)
        self.save(session=session)
        del updated_values['updated_at']
        return updated_values


class Patient(DB.Model, AppBase):
    __tablename__ = 'patient_basic_infos'

    id = DB.Column(DB.Integer, primary_key=True,
                   autoincrement=True, comment='主键id')
    user_name = DB.Column(DB.String, nullable=False, comment='用户名')
    uid = DB.Column(DB.String, nullable=False, comment='用户id')
    gender = DB.Column(DB.String, nullable=False, comment='性别')
    age = DB.Column(DB.Numeric(3), nullable=False, comment='年龄')
    height = DB.Column(DB.Numeric(5, 2), comment='身高')
    weight = DB.Column(DB.Numeric(5, 2), comment='体重')
    job = DB.Column(DB.String, comment='职业')
    edu = DB.Column(DB.String, comment='学历')
    special = DB.Column(DB.String, nullable=False, default="无", comment='特殊情况')
    tel = DB.Column(DB.String, comment='电话')
    tumor = DB.Column(DB.String, nullable=False, default="无", comment='肿瘤')
    tumor_metastasis = DB.Column(DB.String, comment='肿瘤转移')
    tumor_treatment = DB.Column(DB.String, comment='肿瘤治疗')
    illness = DB.Column(DB.String, comment='基础疾病')
    liver_function = DB.Column(DB.String, comment='肝功能')
    kidney_function = DB.Column(DB.String, comment='肾功能')
    cardiac_function = DB.Column(DB.String, comment='心功能')
    allergy = DB.Column(DB.String, comment='过敏史')
    physical_q1 = DB.Column(DB.String, comment='身体状况Q1')
    physical_q2 = DB.Column(DB.String, comment='身体状况Q2')
    physical_q3 = DB.Column(DB.String, comment='身体状况Q3')
    physical_q4 = DB.Column(DB.String, comment='身体状况Q4')
    physical_q5 = DB.Column(DB.String, comment='身体状况Q5')
    physical_score = DB.Column(DB.String, comment='身体状况得分')

    diagnostics = relationship(
        "Diagnostic", back_populates="patient_basic_info")

    def to_brief_info(self):
        return {
            "user_name": self.user_name,
            "uid": self.uid,
            "gender": self.gender,
            "age": int(self.age),
            "physical_score": self.physical_score
        }

    # def to_json(self):
    #     return {
    #         "id": self.id,
    #         "username": self.username,
    #         "email": self.email
    #     }


class Diagnostic(DB.Model, ModelBase, TimestampMixin):
    __tablename__ = 'diagnostics'

    id = DB.Column(DB.Integer, primary_key=True,
                   autoincrement=True, comment='主键id')
    uuid = DB.Column(DB.String(36), nullable=False, comment='uuid')
    patient_basic_info_id = DB.Column(DB.Integer, DB.ForeignKey("patient_basic_infos.id"),
                                      nullable=False,
                                      comment='关联用户基本信息表id')
    pain_assessment_info_id = DB.Column(DB.Integer, comment='关联疼痛评估表id')
    prev_medication_info_id = DB.Column(DB.Integer, comment='关联既往用药信息id')
    decision_info_id = DB.Column(DB.Integer, comment='关联决策信息id')
    doctor_id = DB.Column(DB.Integer, nullable=False,
                          default=0, comment='医师id')
    previous_medication_issue = DB.Column(
        DB.String, nullable=False, default="", comment='既往用药存在问题及原因')
    recmd = DB.Column(DB.String, nullable=False,
                      default="", comment='系统用药决策方案推荐')
    feedback_score = DB.Column(DB.Integer, comment='用户反馈评分')
    request_ip = DB.Column(DB.String, comment='请求ip')

    patient_basic_info = relationship(
        "Patient", uselist=False, back_populates="diagnostics")


class PainAssessmentInfo(DB.Model, ModelBase):
    __tablename__ = 'pain_assessment_infos'

    id = DB.Column(DB.Integer, primary_key=True,
                   autoincrement=True, comment='主键id')
    diagnostic_uuid = DB.Column(DB.String(36), nullable=False, comment='关联诊断表uuid')
    causes = DB.Column(DB.String, nullable=False, comment='疼痛原因 0-肿瘤、1-肿瘤治疗、2-非肿瘤相关性')
    body_parts = DB.Column(DB.String, comment='疼痛部位 对应人体部位表 多选')
    pain_extra = DB.Column(DB.String, default='', comment='其他疼痛说明')
    pain_score = DB.Column(DB.Integer, comment='疼痛ID评分')
    character = DB.Column(DB.String, nullable=False, comment='疼痛性质 多选')
    level = DB.Column(DB.Integer, nullable=False, comment='疼痛强度 单选')
    aggravating_factors = DB.Column(
        DB.String, nullable=False,
        comment='疼痛加重因素 多选 0-行走、1-活动、2-体位变化、3-排便、4-咳嗽、5-进食、6-天气、7-乏力、8-精神因素')
    relief_factors = DB.Column(
        DB.String, nullable=False,
        comment='疼痛缓解因素 多选 0-服用镇痛药、1-环境安静、2-光线柔和、3-温度适宜、4-心理积极、5-家人陪伴')
    breakout_type = DB.Column(
        DB.String, nullable=False,
        comment='爆发痛类型 0-与特定活动或事件相关联、1-发生在按时给予镇痛药物的剂量间隔结束时、2-控制不佳的持续性疼痛 3-无')
    breakout_freq = DB.Column(DB.String, nullable=False, comment='爆发痛发作频率 0-<3、1-≥3')
    illness = DB.Column(DB.String, comment='疼痛相关疾病史 多选 1-心源性哮喘、2-高血压、3-糖尿病、4-心血管事件史、5-消化道出血、6-消化道溃疡、-1-其他')
    symptom = DB.Column(DB.String, comment='症状 1-咳嗽、2-寒颤')


class PreviousMedicationInfo(DB.Model, ModelBase):
    __tablename__ = 'previous_medication_infos'

    id = DB.Column(DB.Integer, primary_key=True,
                   autoincrement=True, comment='主键id')
    uuid = DB.Column(DB.String(36), nullable=False, comment='uuid')
    diagnostic_uuid = DB.Column(DB.String(36), comment='关联诊断表uuid')
    compliance_q1 = DB.Column(DB.String, comment='是否忘记用药 1-是 ，0-否')
    compliance_q2 = DB.Column(DB.String, comment='是否不注意用药 1-是 ，0-否')
    compliance_q3 = DB.Column(DB.String, comment='是否自行停药 1-是 ，0-否')
    compliance_q4 = DB.Column(DB.String, comment='症状更糟时是否曾停止服药 1-是 ，0-否')
    adverse_reaction = DB.Column(
        DB.String, comment='不良反应 1 无 2便秘 3恶心呕吐4 谵妄 5过度镇静6 皮肤瘙痒7 呼吸抑制 8其他')
    adverse_reaction_drugs = DB.Column(DB.String, comment='不良反应用药')
    drug_table_id = DB.Column(DB.Integer, comment='用药表id')


class DecisionInfo(DB.Model, ModelBase):
    __tablename__ = 'decision_infos'

    id = DB.Column(DB.Integer, primary_key=True,
                   autoincrement=True, comment='主键id')
    uuid = DB.Column(DB.String(36), nullable=False, comment='uuid')
    diagnostic_uuid = DB.Column(DB.String(36), comment='关联诊断表uuid')
    drug_table_id = DB.Column(DB.Integer, comment='关联用药表id')
    previous_medication_issue = DB.Column(DB.String, comment='既往用药存在问题及原因')
    recmd = DB.Column(DB.String, comment='系统用药决策方案推荐')
    recmd_constraint = DB.Column(DB.Boolean, comment='是否取消推荐药品的约束')
    pcne_constraint = DB.Column(DB.Boolean, comment='是否取消PCNE检查约束')


class PrescriptionBase(object):
    id = Column(Integer, primary_key=True, autoincrement=True, comment='id')
    drug_name = Column(String, comment='用药名称')
    spec = Column(String, comment='用药含量')
    dose = Column(Float, comment='单次用药剂量')
    dose_unit = Column(String, comment='用药剂量单位')
    freq = Column(String, comment='频次')
    freq_unit = Column(
        String, comment='频次单位 0-一天几次，1-每个几个小时/次，2-多少天/贴3-必要时，4-每晚')
    duration = Column(String, comment='用药起止时长 0>7天，1<=7天')


class PreviousPrescription(DB.Model, ModelBase, PrescriptionBase):
    __tablename__ = 'previous_prescriptions'
    prev_medication_uuid = Column(Integer, comment='关联既往用药表id')


class Prescription(DB.Model, ModelBase, PrescriptionBase):
    __tablename__ = 'prescriptions'
    decision_uuid = Column(Integer, comment='关联决策表id')


class Drug(DB.Model, ModelBase):
    __tablename__ = 'drugs'

    id = DB.Column(DB.Integer, primary_key=True,
                   autoincrement=True, comment='主键id')
    drug_id = DB.Column(DB.String, comment='药品编号')
    drug_name = DB.Column(DB.String, comment='药品名称')
    spec = DB.Column(DB.String, comment='药品含量')
    unit = DB.Column(DB.String, comment='药品含量单位')
    category = DB.Column(DB.String, comment='药品类别(L1-L9)')
    high_dose = DB.Column(DB.String, comment='药品每天最高服用量')
    exce_freq = DB.Column(DB.String, comment='每天服用次数')


class DrugKind(DB.Model):
    __tablename__ = 'drug_kinds'

    id = DB.Column(DB.Integer, primary_key=True,
                   autoincrement=True, comment='主键id')
    drug_category = DB.Column(DB.String, comment='种类')
    drug_desc = DB.Column(DB.String, comment='描述')
    drug_prop = DB.Column(
        DB.String, comment='代号药品属性  1非甾体类，2抗惊厥/抗抑郁药（口服类），3阿片类药物 ，4苯二氮卓类（口服类），5不良反应用药')


class Doctor(DB.Model):
    __tablename__ = 'doctors'

    id = DB.Column(DB.Integer, primary_key=True,
                   autoincrement=True, comment='主键id')
    doctor_name = DB.Column(DB.String, comment='医师名称')
    doctor_job = DB.Column(DB.String, comment='医师职位')
    doctor_dept = DB.Column(DB.String, comment='医师部门')
    doctor_role = DB.Column(DB.Integer, comment='管理权限')
    user_name = DB.Column(DB.String, comment='登录名称')
    user_pwd = DB.Column(DB.String, comment='用户密码')


class AdeCase(DB.Model, AppBase):
    __tablename__ = 'ade_case'
    pid = DB.Column(DB.Integer, primary_key=True,
                    autoincrement=True, comment='主键id')
    name = DB.Column(DB.String, comment='姓名')
    id = DB.Column(DB.String, comment='身份证号')
    tel = DB.Column(DB.String, comment='电话')
    gender = DB.Column(DB.String, comment='性别')
    age = DB.Column(DB.Integer, comment='年龄')
    height = DB.Column(DB.Float, comment='身高')
    weight = DB.Column(DB.Float, comment='体重')
    primary_tumor_diagnosis = DB.Column(DB.String, comment='原发肿瘤诊断')
    pain_type = DB.Column(DB.String, comment='疼痛类型')
    pain_nature = DB.Column(DB.String, comment='疼痛性质')
    pain_level = DB.Column(DB.Integer, comment='疼痛程度')
    cs_drugs = DB.Column(DB.String, comment='心脑血管系统药物')
    bmi = DB.Column(DB.String, comment='BMI')
    smoking_history = DB.Column(DB.String, comment='吸烟史')
    kps = DB.Column(DB.String, comment='KPS评分')
    opiate_tolerant = DB.Column(DB.String, comment='阿片耐受度')
    serum_creatinine = DB.Column(DB.String, comment='血肌酐')
    rs1074287 = DB.Column(DB.String, comment='rs1074287基因型')
    proba = DB.Column(DB.Float, comment='事件发生概率')
