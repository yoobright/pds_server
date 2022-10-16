from db import DB as db_cls
from db import models

DB = db_cls.db

def add_patient(values):
    user = models.Patient()
    user.update(values)
    DB.session.add(user)
    DB.session.commit()

    return user


def get_all_patients(values):
    query = DB.session.query(models.Patient)
    if values is not None and values.user_name:
        query = query.filter(models.Patient.user_name == values.user_name)

    users = query.all()

    return users


def get_patient_by_id(uid):
    user = DB.session.query(models.Patient).\
        filter(models.Patient.id == uid).one_or_none()

    return user


def delete_patient_by_id(uid):
    res = DB.session.query(models.Patient).\
        filter(models.Patient.id == uid).delete()
    DB.session.commit()

    return res


def update_patient_by_id(uid, values):
    user = DB.session.query(models.Patient).\
        filter(models.Patient.id == uid).one_or_none()

    if user is not None:
        user.update(values)
        DB.session.commit()

    return user

def add_drug(values):
    drug = models.Drug()
    drug.update(values)
    DB.session.add(drug)
    DB.session.commit()

    return drug