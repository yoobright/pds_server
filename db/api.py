from db import db
from db import models


def add_patient(values):
    user = models.Patient()
    user.update(values)
    db.session.add(user)
    db.session.commit()

    return user


def get_all_patients(values):
    query = db.session.query(models.Patient)
    if values.user_name:
        query = query.filter(models.Patient.user_name == values.user_name)

    users = query.all()

    return users


def get_patient_by_id(uid):
    user = db.session.query(models.Patient).\
        filter(models.Patient.id == uid).one_or_none()

    return user


def delete_patient_by_id(uid):
    res = db.session.query(models.Patient).\
        filter(models.Patient.id == uid).delete()
    db.session.commit()

    return res


def update_patient_by_id(uid, values):
    user = db.session.query(models.Patient).\
        filter(models.Patient.id == uid).one_or_none()

    if user is not None:
        user.update(values)
        db.session.commit()

    return user

