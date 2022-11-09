import uuid

from sqlalchemy import desc

from db import DB_Obj
from db import models


DB = DB_Obj.db


def add_patient(values):
    patient = models.Patient()
    patient.update(values)
    DB.session.add(patient)
    DB.session.commit()

    return patient


def get_all_patients(values=None):
    query = DB.session.query(models.Patient)
    if values is not None and values.user_name:
        query = query.filter(models.Patient.user_name == values.user_name)

    patients = query.all()

    return patients


def get_patient_by_id(pid):
    patient = DB.session.query(models.Patient).\
        filter(models.Patient.id == pid).one_or_none()

    return patient


def delete_patient_by_id(pid):
    res = DB.session.query(models.Patient).\
        filter(models.Patient.id == pid).delete()
    DB.session.commit()

    return res


def update_patient_by_id(pid, values):
    patient = DB.session.query(models.Patient).\
        filter(models.Patient.id == pid).one_or_none()

    if patient is not None:
        patient.update(values)
        DB.session.commit()

    return patient


def add_drug(values):
    drug = models.Drug()
    drug.update(values)
    DB.session.add(drug)
    DB.session.commit()

    return drug


def get_all_drugs(values=None):
    query = DB.session.query(models.Drug)
    drugs = query.all()

    return drugs


def add_diagnostic(values):
    patient_basic_info_id = values.get('patient_basic_info_id', None)
    if patient_basic_info_id is None:
        return None
    patient = get_patient_by_id(patient_basic_info_id)
    if patient is None:
        return None
    
    diagnostic = models.Diagnostic()
    diagnostic.update(values)
    if diagnostic.uuid is None:
        diagnostic.uuid = str(uuid.uuid4())
    diagnostic.patient_basic_info = patient

    DB.session.add(diagnostic)

    DB.session.commit()

    return diagnostic


def get_all_diagnostics(values=None):
    query = DB.session.query(models.Diagnostic)\
        .order_by(desc(models.Diagnostic.created_at))
    diagnostics = query.all()

    return diagnostics


def add_pain_assessment(values=None):
    diagnostic = DB.session.query(models.Diagnostic)\
        .filter(models.Diagnostic.uuid == values.diagnostic_uuid).one_or_none()
    if diagnostic is None:
        return None
    pain_assessment = models.PainAssessmentInfo()
    pain_assessment.update(values)
    DB.session.add(pain_assessment)
    DB.session.commit()

    diagnostic.pain_assessment_info_id = pain_assessment.id
    DB.session.commit()

    return pain_assessment

def add_decision(values):
    diagnostic = DB.session.query(models.Diagnostic)\
        .filter(models.Diagnostic.uuid == values.diagnostic_uuid).one_or_none()
    if diagnostic is None:
        return None

    decision = models.DecisionInfo()
    decision.update(values)
    DB.session.add(decision)
    DB.session.commit()

    diagnostic.decision_info_id = decision.id
    DB.session.commit()

    return decision


def rebuild_drug_table():
    models.Drug.__table__.drop(DB.engine)
    models.Drug.__table__.create(DB.engine)
