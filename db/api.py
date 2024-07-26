import uuid

from sqlalchemy import desc
from sqlalchemy.orm import defer

from db import DB_Obj
from db import models

DB = DB_Obj.db


def add_page_query(args, query):
    page = args.get("page", None)
    limit = args.get("limit", None)
    if page is not None and limit is not None:
        query = query.limit(limit).offset((page - 1) * limit)
    return query


def add_patient(values):
    patient = models.Patient()
    patient.update(values)
    DB.session.add(patient)
    DB.session.commit()

    return patient


def get_all_patients(values=None):
    query = DB.session.query(models.Patient)
    user_name = values.get("user_name", None)
    if values is not None and user_name:
        query = query.filter(models.Patient.user_name == user_name)

    patients = query.all()

    return patients


def get_patient_by_id(pid):
    patient = DB.session.query(models.Patient). \
        filter(models.Patient.id == pid).one_or_none()

    return patient


def delete_patient_by_id(pid):
    res = DB.session.query(models.Patient). \
        filter(models.Patient.id == pid).delete()
    DB.session.commit()

    return res


def update_patient_by_id(pid, values):
    patient = DB.session.query(models.Patient). \
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


def get_all_drugs(args=None):
    query = DB.session.query(models.Drug)

    drug_name = args.get("drug_name", None)
    if drug_name is not None:
        search_name = "{}%".format(drug_name)
        query = query.filter(models.Drug.drug_name.like(search_name))

    total = query.count()

    query = add_page_query(args, query)
    drugs = query.all()

    return drugs, total


def add_diagnostic(values, request_ip):
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
    diagnostic.request_ip = request_ip
    diagnostic.patient_basic_info = patient

    DB.session.add(diagnostic)

    DB.session.commit()

    return diagnostic


def get_all_diagnostics(args):
    query = DB.session.query(models.Diagnostic)

    user_name = args.get("user_name", None)
    if user_name is not None:
        search_name = "{}%".format(user_name)
        query = query.join(models.Patient, models.Patient.id ==
                           models.Diagnostic.patient_basic_info_id)\
            .filter(models.Patient.user_name.like(search_name))
    query = query.order_by(desc(models.Diagnostic.created_at))

    total = query.count()

    query = add_page_query(args, query)
    diagnostics = query.all()

    return diagnostics, total


def gen_drug_table(drugs):
    drug_table = []
    for d in drugs:
        drug_table.append(
            {
                "drug_name": d.drug_name,
                "spec": d.spec,
                "dose": d.dose,
                "dose_unit": d.dose_unit,
                "freq": d.freq,
                "freq_unit": d.freq_unit,
                "duration": d.duration
            }
        )
    return drug_table


def to_diagnostic_detail(diagnostic):
    if diagnostic is not None:
        print(diagnostic.patient_basic_info)
        if diagnostic.pain_assessment_info_id is not None:
            pain_assessment = DB.session.query(models.PainAssessmentInfo) \
                .filter(models.PainAssessmentInfo.diagnostic_uuid == diagnostic.uuid) \
                .order_by(models.PainAssessmentInfo.id.desc()) \
                .first()
            if pain_assessment is not None:
                diagnostic['pain_assessment_info'] = dict(
                    pain_assessment.items())

        if diagnostic.prev_medication_info_id is not None:
            prev_medication = DB.session.query(models.PreviousMedicationInfo) \
                .filter(models.PreviousMedicationInfo.diagnostic_uuid == diagnostic.uuid) \
                .order_by(models.PreviousMedicationInfo.id.desc()) \
                .first()
            if prev_medication is not None:
                drugs = DB.session.query(models.PreviousPrescription) \
                    .options(defer(models.PreviousPrescription.prev_medication_uuid)) \
                    .filter(models.PreviousPrescription.prev_medication_uuid ==
                            prev_medication.uuid) \
                    .all()
                drug_table = gen_drug_table(drugs)
                prev_medication['drug_table'] = drug_table

                diagnostic['prev_medication_info'] = dict(
                    prev_medication.items())

        if diagnostic.decision_info_id is not None:
            decision = DB.session.query(models.DecisionInfo) \
                .filter(models.DecisionInfo.diagnostic_uuid == diagnostic.uuid) \
                .order_by(models.DecisionInfo.id.desc()) \
                .first()
            if decision is not None:
                drugs = DB.session.query(models.Prescription) \
                    .options(defer(models.Prescription.decision_uuid)) \
                    .filter(models.Prescription.decision_uuid ==
                            decision.uuid) \
                    .all()
                drug_table = gen_drug_table(drugs)
                decision['drug_table'] = drug_table
                diagnostic['decision_info'] = dict(decision.items())

    return diagnostic


def get_diagnostic_by_uuid(uuid):
    diagnostic = DB.session.query(models.Diagnostic) \
        .filter(models.Diagnostic.uuid == uuid).first()

    return to_diagnostic_detail(diagnostic)


def get_diagnostic_by_patient(args):
    user_name = args.get("user_name", None)
    uid = args.get("uid", None)
    if user_name is None or uid is None:
        return None

    patient_id = DB.session.query(models.Patient.id) \
        .filter(models.Patient.user_name == user_name) \
        .filter(models.Patient.uid == uid) \
        .order_by(models.Patient.id.desc()) \
        .first()

    if patient_id is None:
        return None
    patient_id = patient_id[0]
    print(patient_id)
    if args.get("latest", False):
        diagnostic = DB.session.query(models.Diagnostic) \
            .filter(models.Diagnostic.patient_basic_info_id == patient_id) \
            .order_by(models.Diagnostic.id.desc()) \
            .first()
        return to_diagnostic_detail(diagnostic)
    else:
        query = DB.session.query(models.Diagnostic) \
            .filter(models.Diagnostic.patient_basic_info_id == patient_id) \
            .order_by(models.Diagnostic.id.desc())

        # if args.page is not None and args.limit is not None:
        #     query = query.limit(args.limit).offset((args.page - 1) * args.limit)

        diagnostics = query.all()

        return diagnostics


def update_diagnostic_by_uuid(uuid, args):
    diagnostic = DB.session.query(models.Diagnostic) \
        .filter(models.Diagnostic.uuid == uuid) \
        .order_by(models.Diagnostic.id.desc()) \
        .first()
    if diagnostic is not None:
        diagnostic.update(args)
        DB.session.commit()

    return diagnostic


def add_pain_assessment(values=None):
    diagnostic_uuid = values.get('diagnostic_uuid', None)
    diagnostic = DB.session.query(models.Diagnostic) \
        .filter(models.Diagnostic.uuid == diagnostic_uuid).one_or_none()
    if diagnostic is None:
        return None
    pain_assessment = models.PainAssessmentInfo()
    pain_assessment.update(values)
    DB.session.add(pain_assessment)
    DB.session.commit()

    diagnostic.pain_assessment_info_id = pain_assessment.id
    DB.session.commit()

    return pain_assessment


def add_previous_medication(values):
    diagnostic_uuid = values.get('diagnostic_uuid', None)
    diagnostic = DB.session.query(models.Diagnostic) \
        .filter(models.Diagnostic.uuid == diagnostic_uuid).one_or_none()
    if diagnostic is None:
        return None
    previous_medication = models.PreviousMedicationInfo()
    previous_medication.update(values)
    previous_medication_uuid = uuid.uuid4()
    previous_medication.uuid = str(previous_medication_uuid)

    DB.session.add(previous_medication)

    drug_table = values.get('drug_table', None)
    if drug_table is not None:
        for d in drug_table:
            prescription = models.PreviousPrescription()
            prescription.update(d)
            prescription.prev_medication_uuid = str(previous_medication_uuid)
            DB.session.add(prescription)
    DB.session.commit()

    diagnostic.prev_medication_info_id = previous_medication.id
    DB.session.commit()

    return previous_medication


def add_decision(values):
    diagnostic_uuid = values.get('diagnostic_uuid', None)
    diagnostic = DB.session.query(models.Diagnostic) \
        .filter(models.Diagnostic.uuid == diagnostic_uuid).one_or_none()
    if diagnostic is None:
        return None

    decision_uuid = uuid.uuid4()
    decision = models.DecisionInfo()
    decision.update(values)
    decision.uuid = str(decision_uuid)
    DB.session.add(decision)

    drug_table = values.get('drug_table', None)
    if drug_table is not None:
        for d in drug_table:
            prescription = models.Prescription()
            prescription.update(d)
            prescription.decision_uuid = str(decision_uuid)
            DB.session.add(prescription)
    DB.session.commit()

    diagnostic.decision_info_id = decision.id
    diagnostic.previous_medication_issue = decision.previous_medication_issue
    diagnostic.recmd = decision.recmd

    DB.session.commit()

    return decision


def add_ade_case(values):
    for k, v in values.items():
        if type(v) is list:
            values[k] = ",".join(v)
    ade_case = models.AdeCase()
    ade_case.update(values)
    DB.session.add(ade_case)
    DB.session.commit()
    return ade_case

def get_all_ade_case():
    all_ade_case = DB.session.query(models.AdeCase).all()
    return all_ade_case


def rebuild_drug_table():
    models.Drug.__table__.drop(DB.engine)
    models.Drug.__table__.create(DB.engine)
